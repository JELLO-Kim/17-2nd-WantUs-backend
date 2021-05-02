import json
from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Count

from .models        import (
        Apply,
        ProcessStatus
        )
from user.models    import User
from utils          import login_decorator
from resume.models  import Resume, ResumeFile
from posting.models import (
        Posting,
        Occupation,
        JobCategory,
        CompanyImage,
        CompanyDetail,
        State,
        County,
        Tag,
        TagDetail,
        CompanyTag,
        BookMark,
        Like,
        Company,
        )

class ApplyView(View):
    @login_decorator
    def get(self, request):
        """[Apply] 유저가 "지원하기" 눌렀을시 유저의 정보와 이력서 목록 반환
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
        Return:
            - 200: 'message':'SUCCESS', 'data': 유저의 정보 + 이력서 목록}
        """
        user = request.user

        resumes     = Resume.objects.filter(user=user).values(\
                        'id', 'user_id', 'title', 'introduce', 'create_at')
        resume_file = ResumeFile.objects.filter(user=user).values(\
                        'id', 'user_id', 'title', 'file_url', 'create_at')
        
        resume_result = []

        for resume in resumes.union(resume_file).order_by('-create_at'):
            result = {
                'id'        : resume.id,
                'userId'    : resume.user_id,
                'title'     : resume.title,
                'createAt'  : resume.create_at,
                'introduce' : resume.introduce if resume.get('introduce') else '',
                'file_url'  : resume.file_url if resume.get('file_url') else '',
            }
            resume_result.append(result)

        data = {
            'name'        : user.name,
            'email'       : user.email,
            'phoneNumber' : user.phone_number,
            'resumes'     : resume_result
        }

        return JsonResponse({'message':'SUCCESS', 'data':data}, status=200)

    @login_decorator
    def post(self, request):
        """[Apply] 채용 상세페이지에서 "지원하기"
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
            - posting: body에 담겨오는 지원하는 채용공고의 id
        Return:
            - 201: {'message':'SUCCESS'}
            - 400 (채용공고가 유효하지 않습니다): body에 채용공고의 id가 담겨있지 않을 경우
        Note:
            - 어떤 이력서로 지원하였는지에 대한 기록하는 column 존재하지 않음.
        """
        data = json.loads(request.body)

        user    = request.user
        posting = data.get('posting', None)

        if not posting:
            return JsonResponse({'message':'채용공고가 유효하지 않습니다.'}, status=400)
        
        # "누가" "어떤" 공고에 지원하였는가를 기록한다.
        Apply.objects.create(
            user = user,
            posting_id = posting
        )

        return JsonResponse({'message':'SUCCESS'}, status=200)

class MyWantUsView(View):
    @login_decorator
    def get(self, request):
       """[Apply] 로그인 유저의 마이페이지 화면
        Args:
            - user : requset의 Header에 담겨져 오는 token으로 회원 유효성 검사 후 user객체 반환
        Return:
            - 200: {
                    'user' : 로그인 유저의 정보,
                    "apply" : 로그인 유저의 지원 현황,
                    "book" : 로그인 유저가 북마크한 공고,
                    "like" : 로그인 유저가 좋아요한 공고
                    }
        Note:
            - "좋아요" 한 공고와 "북마크"한 공고의 내역이 다르게 보임
        """
        user    = request.user
        user_info = {
                'profile'       : user.image_url,
                'name'          : user.name,
                'email'         : user.email,
                'phoneNumber'   : user.phone_number
                }
        FIRST  = '지원 완료'
        SECOND = '서류 통과'
        THIRD  = '최종 합격'
        FOURTH = '불합격'

        apply_list = {
                "stepOne"   : user.apply_set.filter(process_status__name = FIRST).count(),
                "stepTwo"   : user.apply_set.filter(process_status__name = SECOND).count(),
                "stepThree" : user.apply_set.filter(process_status__name = THIRD).count(),
                "stepFour"  : user.apply_set.filter(process_status__name = FOURTH).count()
                }

        # datetime 형식 가공
        DATETIME_ONLY_TIME = 10
        book_mark_posting = [{
            'id'            : posting.id,
            'category'      : posting.job_category.occupation.name,
            'city'          : posting.company_detail.state.name,
            'company'       : posting.company_detail.company.name,
            'end'           : str(posting.end_date)[:DATETIME_ONLY_TIME],
            'image'         : posting.company_detail.company.companyimage_set.first().image_url,
            'state'         : posting.company_detail.county.name,
            'subCategory'   : posting.job_category.name,
            'tags'          : [TagDetail.objects.get(id=tag_detail_id_dict['tag_detail_id']).name
                                for tag_detail_id_dict in posting.company_detail.company.companytag_set.values()],
            'title'         : posting.title,
            } for posting in Posting.objects.filter(bookmark__user = user)]
        
        like_posting = [{
            'id'        : posting.id,
            'city'      : posting.company_detail.state.name,
            'company'   : posting.company_detail.company.name,
            'image'     : posting.company_detail.company.companyimage_set.first().image_url,
            'state'     : posting.company_detail.county.name,
            'title'     : posting.title,
            } for posting in Posting.objects.filter(like__user=user)]

        return JsonResponse({'user' : user_info, "apply" : apply_list, "book" : book_mark_posting, "like" : like_posting}, status=200)