import json
import jwt
import requests
from json.decoder   import JSONDecodeError

from django.http  import JsonResponse
from django.views import View

from my_settings  import SECRET_KEY, ALGORITHM
from utils          import login_decorator
from posting.models import (
    Occupation,
    JobCategory,
)
from user.models    import (
    WorkExperience,
    Skill,
    User
)

class SignView(View):
    def get(self, request):
        """
        Args:
            - Authorization: kakaoTalk API로 소셜로그인 진행 시 kakaoTalk에서 발급해 주는 전용 token
        Return:
            - 200 (기존에 회원가입된 유저일 경우 로그인 진행) : {'message' : 'SUCCESS', 'accessToken' : 우리 API에서 발급해준 access_token}
            - 201 (신규 회원일 경우 회원가입과 동시에 로그인 진행): {'message' : 'SUCCESS', 'accessToken' : 우리 API에서 발급해준 access_token}
        """
        try:
            kakao_token  = request.headers["Authorization"]
            headers      = {'Authorization' : f"Bearer {kakao_token}"}
            url          = "https://kapi.kakao.com/v2/user/me"
            response     = requests.request("GET", url, headers=headers)
            user         = response.json()

            if User.objects.filter(email = user['kakao_account']['email']).exists(): 
                user_info   = User.objects.get(email=user['kakao_account']['email'])
                encoded_jwt = jwt.encode({'id': user_info.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'message':'SUCCESS', 'accessToken' : encoded_jwt}, status = 200)
            
            new_user_info = User.objects.create(
                email     = user['kakao_account']['email'],
                name      = user['kakao_account']['profile']['nickname'],
                image_url = user['kakao_account']['profile'].get('profile_image_url', ''),
            )
            
            encoded_jwt = jwt.encode({'id': new_user_info.id}, SECRET_KEY, algorithm=ALGORITHM)
            return JsonResponse({'message':'SUCCESS', 'accessToken' : encoded_jwt}, status = 201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
            
class ProfileView(View):
    @login_decorator
    def patch(self, request):
        """[User] 마이페이지에서 로그인 유저의 상세정보 수정
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
            - name: 수정하고자 하는 이름. 없을 경우 기존의 이름으로 지정
            - workExperince: 수정하고자 하는 경력 사항. 없을 경우 기존의 경력으로 지정.
            - salary: 수정하고자 하는 연봉 정보. 없을 경우 기존의 연봉 정보로 지정.
            - phoneNumber: 수정하고자 하는 핸드폰 번호. 없을 경우 기존의 핸드폰 번호로 지정.
        Return:
            - 201: {'message':'SUCCESS'}
        Note:
            - 새로운 기술스택과 업무직군 변동은 "추가" 만 가능
        """
        try:
            data = json.loads(request.body)

            user            = request.user
            name            = data.get('name', user.name)
            work_experience = data.get('workExperience', user.work_experience) # 신입/경력
            salary          = data.get('salary', user.salary)
            phone_number    = data.get('phoneNumber', user.phone_number)

            user.name            = name
            user.work_experience = work_experience
            user.salary          = salary
            user.phone_number    = phone_number

            # 수정 내용을 반영하여 새롭게 저장
            user.save()

            # 새로운 기술스택이 추가될 경우
            for skill in data.get('skills', []):
                user.skill.add(skill)
            
            # 새로운 업무직군이 추가될 경우
            for job in data.get('jobCategory', []):
                user.job_category.add(job)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        return JsonResponse({'message':'SUCCESS'}, status=201)