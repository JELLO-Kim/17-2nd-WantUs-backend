import json
import uuid
import boto3
import urllib.request

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Count, Prefetch

from my_settings    import S3KEY, S3SECRETKEY
from user.models    import User
from resume.models  import (
        ResumeFile,
        Resume,
        ResumeStatus,
        Career,
        Language,
        Education
        )
from utils         import login_decorator

class ResumeFilewUploadView(View):
    @login_decorator
    def post(self, request):
        """[Resume] 외부 이력서 업로드하기 (S3 사용)
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
        Return:
            - 200: {'message': 'SUCCESS', 'data': 우리 DB에 저장된 file의 주소}
        Note:
            - file 명과 확장자명으로 file 유효성을 판단
        """
        user = request.user
        user = User.objects.get(id=4)
        # 빈 파일일 경우 (파일명의 길이가 0일 경우) validation
        if request.FILES.__len__() == 0:
            return JsonResponse({"message": "FILE_DOES_NOT_EXIST"}, status=400)

        file = request.FILES['resume']
        # file의 형식이 pdf인지 확인하는 validation (확장자명이 pdf가 아닐때 에러반환)
        if file.name.find('pdf') < 0:
            return JsonResponse({"message": "PLEASE_UPLOAD_PDF"}, status=400)
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id = S3KEY,
            aws_secret_access_key = S3SECRETKEY
            )
        # uuid를 통해 최대한 유니크한 랜덤의 문자열 생성
        url_generator = str(uuid.uuid4())
        s3_client.upload_fileobj(
                file,  
                "wantusfile",
                url_generator,
                ExtraArgs = {
                    "ContentType": file.content_type,
                    }
                )
        file_url = f"https://wantusfile.s3.ap-northeast-2.amazonaws.com/{url_generator}"
        resume   = ResumeFile.objects.create(user=user, title=file.name, file_url=file_url, uuidcode=url_generator)
        return JsonResponse({'message': 'SUCCESS', 'data': file_url}, status=200)
    
    @login_decorator
    def delete(self, request, resume_id):
        """[Resume] 외부 이력서 삭제하기 (S3 사용)
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
            - resume_id : path parameter로 들어오는 지우고자 하는 이력서의 id 값
        Return:
            - 200: {'message': 'SUCCESS'}
        """
        try:
            resume    = ResumeFile.objects.get(id=resume_id)
            key       = resume.uuidcode
            file_url  = resume.file_url
            urllib.request.urlopen(file_url).getcode()
            s3_client = boto3.client(
                                    's3',
                                    aws_access_key_id     = S3KEY,
                                    aws_secret_access_key = S3SECRETKEY
            )
            s3_client.delete_object(Bucket='wantusfile', Key=key)
            resume.delete()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except ResumeFile.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=404)
        
        except urllib.error.URLError:
            return JsonResponse({'message': 'INVALID_URL'}, status=404)

class ResumeView(View):
    @login_decorator
    def get(self, request):
        """[Resume] 유저의 모든 이력서
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
        Return:
            - 200: {'message': 'SUCCESS', 'result' : 이력서 목록}
        Note:
            - 기본제공 이력서와 외부파일 업로드 이력서 모두 반환해야 하므로 두종류 data를 합치는 과정에서 values() 메소드 사용
            - 최신 생성순으로 정렬
        """
        user    = request.user
        # 기본제공 이력서
        resumes = Resume.objects.filter(user=user).values('id', 'title', 'update_at', 'complete_status', 'is_default')
        # 외부파일 업로드 이력서
        resume_files = ResumeFile.objects.filter(user=user).values('id', 'title', 'update_at', 'complete_status', 'is_default')
        # 두가지 값을 합쳐 하나의 list로 생성
        resume_list = [{
            "id"     : resume['id'],
            "name"   : resume['title'],
            "date"   : resume['update_at'],
            "status" : ResumeStatus.objects.get(id=resume['complete_status']).status_code,
            "matchUp" : resume['is_default']
            } for resume in resumes.union(resume_files).order_by('-update_at')]

        return JsonResponse({'message' : 'SUCCESS', 'result' : resume_list}, status=200)

    @login_decorator
    def post(self, request):
        """[Resume] 유저의 기본제공 이력서 새로 생성
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
        Return:
            - 200: {'message': 'SUCCESS', 'result' : 새로 생성된 이력서의 id}
        Note:
            - DB에 저장된 해당 유저의 이력서 갯수 +1만큼 하여 새 이력서의 이름 생성
        """
        user   = request.user
        resume = Resume.objects.create(
                user    = user,
                title   = f'{user.name}'+str(Resume.objects.filter(user=user).count()+1),
                )
        return JsonResponse({'message' : 'SUCCESS', 'result' : resume.id}, status=201)

class ResumePartialView(View):
    @login_decorator
    def get(self, request, resume_id):
        """[Resume] 유저의 이력서 상세 내역
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
            - resume_id : path paramter로 받는 특정 resume의 id
        Return:
            - 200: {'message' : 'SUCCESS', 'result' : 이력서 세부 내용}
            - 400 (유저의 이력서가 아닙니다): 로그인한 유저의 이력서가 아닐 경우
            - 404 (이력서가 존재하지 않습니다): 유효하지 않는 이력서 id로 접근했을 경우
        Note:
            - DB에 저장된 해당 유저의 이력서 갯수 +1만큼 하여 새 이력서의 이름 생성
        """
        try:
            user                = request.user
            resume              = Resume.objects.get(id=resume_id)
            
            if user.id != resume.user.id:
                return JsonResponse({'message' : '유저의 이력서가 아닙니다'}, status=400)
            
            content = {
                    "userInfo" : {
                        "name"          : user.name,
                        "email"         : user.email,
                        "phoneNumber"   : user.phone_number
                    },
                    "resumeIntro" : resume.introduce,
                    "resumeTitle" : resume.title,
                    "career" : [{
                        "id"      : career.id,
                        "Name"    : career.name,
                        "Start"   : career.start_date,
                        "End" : career.end_date
                        } for career in resume.career_set.all()],
                    "education" : [{
                        "id"       : education.id,
                        "Name"     : education.name,
                        "Start"    : education.start_date,
                        "End"      : education.end_date
                        } for education in resume.education_set.all()],
                    "language" : [{
                        "id"    : language.id,
                        "Name"  : language.name,
                        "Start" : language.start_date,
                        "End"   : language.end_date
                        } for language in resume.language_set.all()]
                }
            return JsonResponse({'message' : 'SUCCESS', 'result' : content}, status=200)
        
        except Resume.DoesNotExist:
            return JsonResponse({'message' : '이력서가 존재하지 않습니다'}, status=404)

    @login_decorator
    def delete(self, request, resume_id):
        """[Resume] 유저의 이력서 한개 삭제하기
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
            - resume_id : path paramter로 받는 특정 resume의 id
        Return:
            - 204: {'message' : '삭제완료'}
            - 400 (유저의 이력서가 아닙니다): 로그인한 유저의 이력서가 아닐 경우
            - 404 (이력서가 존재하지 않습니다): 유효하지 않는 이력서 id로 접근했을 경우
        Note:
            - DB에 저장된 해당 유저의 이력서 갯수 +1만큼 하여 새 이력서의 이름 생성
        """
        try:
            user    = request.user
            resume  = Resume.objects.get(id=resume_id)
            if user.id != resume.user.id:
                return JsonResponse({'message' : '유저의 이력서가 아닙니다'}, status=400)

            resume.delete()
            return JsonResponse({'message' : '삭제완료'}, status=204)

        except Resume.DoesNotExist:
            return JsonResponse({'message' : '이력서가 존재하지 않습니다'}, status=404)


