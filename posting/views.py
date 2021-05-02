import json
import math

from django.core.paginator  import Paginator
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import (
    Count,
    Prefetch,
    Q
)

from posting.models import (
    Posting, 
    CompanyDetail, 
    CompanyTag,
    County,
    State,
    Tag,
    TagDetail,
    JobCategory
)
from user.models            import User
from resume.models          import Resume, ResumeFile, ResumeStatus
from utils                  import login_decorator, non_user_accept_decorator
from posting.models         import (
        Posting,
        Occupation,
        Company,
        CompanyImage,
        CompanyDetail,
        State,
        County,
        Like,
        BookMark,
        CompanyTag,
        Tag,
        TagDetail
)

LIST_LIMIT_NUMBER = 4

class MainView(View):
    @login_decorator
    def get(self, request):
        """
        Return:
            - 200: {
                    'likePisting' : 좋아요 가장많은 4개의 채용공고,
                    'new' : 가장 최근의 채용공고 4건의 주최 회사(중복 허용),
                    'thisWeek' : 가장 최근의 채용공고 4건
                    }
        Note:
            - DB hit을 고려하여 select_related 활용
            - 좋아요 갯수 판단을 위한 annotate메소드 사용        
        """
        set_postings = Posting.objects.annotate(like_num=Count("like")).\
                    select_related('company_detail', 
                            'company_detail__state', 
                            'company_detail__county', 
                            'company_detail__company', 
                            'job_category', 
                            'job_category__occupation').all()

        postings = set_postings.order_by('-like_num')[:LIST_LIMIT_NUMBER]

        like_posting_list = [{
            "postingId" : posting.id,
            "imageUrl"  : posting.company_detail.company.companyimage_set.first().image_url if posting.company_detail.company.companyimage_set.exists() else None,
            "job"       : posting.title,
            "name"      : posting.company_detail.company.name,
            "city"      : posting.company_detail.state.name,
            "state"     : posting.company_detail.county.name,
            "price"     : int(posting.reward),
            "likeNum"   : posting.like_set.filter(posting=posting).count()
            } for posting in postings]

        postings = set_postings.order_by('-create_at')[:LIST_LIMIT_NUMBER]

        new_company_list = [{
            "postingId" : posting.id,
            "imageUrl"  : posting.company_detail.company.companyimage_set.first().image_url if posting.company_detail.company.companyimage_set.exists() else None,
            "name"      : posting.company_detail.company.name,
            "job"       : posting.job_category.occupation.name,
            }for posting in postings]

        new_posting_list = [{
            "imageUrl"  : posting.company_detail.company.companyimage_set.first().image_url if posting.company_detail.company.companyimage_set.exists() else None,
            "postingId" : posting.id,
            "job"       : posting.title,
            "name"      : posting.company_detail.company.name,
            "city"      : posting.company_detail.state.name,
            "state"     : posting.company_detail.county.name,
            "price"     : int(posting.reward),
            } for posting in postings]

        return JsonResponse({"likePosting" : like_posting_list, "new" : new_company_list, "thisWeek" : new_posting_list}, status=200)

class PostingListView(View):
    def get(self, request):
        """
        Args:
            - category : 채용공고 filtering에 필요한 cateogry에 대한 query parameter. 값이 없을 경우 None 지정
            - sorting : 정렬 조건에 필요한 query paratmer. 값이 없을 경우 최신순.
            - tags : 채용공고 filtering에 필요한 tags에 대한 query parameter. 값이 없을 경우 None 지정
            - locations : 채용공고의 위치별 filtering에 필요한 query parameter. 값이 없을 경우 None 지정
            - page : pagination 구현에 필요. 현재의 page 표시. 값이 없으면 1번째 페이지로 지정한다.
            - per_page : pagination 구현에 필요. 한 페이지당 표시할 채용공고의 수. 값이 없으면 30개를 표시하도록 한다.
        Return:
            - 200: {
                    'message' : 'SUCCESS',
                    'data'    : 조건에 맞는 채용공고 list + 위치와 필터, 정렬조건에 대한 데이터들
                }
        """

        q = Q()
        category        = request.GET.get('category', None)
        sorting         = request.GET.get('sorting', 'new')
        tags            = request.GET.getlist('tag', None)
        locations       = request.GET.getlist('location', None)

        # 지정된 category 값이 있을 경우. 카테고리 이름으로 값을 받는다
        if category:
            q.add(Q(job_category__name = category), q.AND)

        query = Posting.objects.filter(q)
        
        # 지정된 값이 있을 경우. 위치 이름으로 값을 받는다. (여러개 선택 가능)
        if locations:
            query = Posting.objects.filter(company_detail__county__name__in=locations)

        # 지정된 값이 있을 경우. 항목 이름으로 값을 받는다. (여러개 선택 가능)
        if tags:
            for tag in tags:
                query = query.filter(company_detail__company__tag__name=tag)
        
        # 정렬 조건에 대한 key_value 값이 담긴 dictionary
        SORTING_DICT = {
            'new'     : '-create_at',
            'popular' : '-like_num',
            'reward'  : '-reward'
        }

        # filtering 완료된 posting의 queryset 에서 정렬조건에 맞춰 다시 배정
        postings = query.select_related\
                    ('company_detail', 'company_detail__company', 'company_detail__state', 'company_detail__county')\
                    .prefetch_related('company_detail__company__companyimage_set', 'company_detail__company__companytag_set')\
                    .annotate(like_num=Count('posting_like'))\
                    .order_by(SORTING_DICT[sorting])

        # pagination 구현 : django의 Paginator 메소드 활용
        page      = request.GET.get('page', 1)
        per_page  = request.GET.get('per_page', 30)
        paginator = Paginator(postings, per_page)

        if paginator.num_pages < int(page):
            return JsonResponse({'message':'NONE_PAGE'}, status=204)

        # django의 메소드에서 자동으로 계산하여 해당 page에 반환해야할 데이터를 담게 한다.    
        postings  = paginator.get_page(page)

        # 위치 조건에 필요
        states      = State.objects.all()
        counties    = County.objects.all()

        # 필터 조건에 필요
        filter_tags = Tag.objects.all()

        data = {
            'postings' : [{
                'id'      : posting.id,
                'like'    : posting.like_set.filter(posting=posting).count(),
                'title'   : posting.title,
                'company' : posting.company_detail.company.name,
                'state'   : posting.company_detail.state.name,
                'county'  : posting.company_detail.county.name,
                'reward'  : posting.reward,
                'image'   : [company_image.image_url for company_image in posting.company_detail.company.companyimage_set.all()]
            } for posting in postings],
            'locations' : {
                'state' : [{
                    'id'   : state.id,
                    'name' : state.name
                } for state in states],
                'county' : [{
                    'id'   : county.id,
                    'name' : county.name
                } for county in counties],
            },
            'tags' : [{
                    'id'   : tag.id,
                    'name' : tag.name,
                    'tagDetails' : [{
                        'id'   : tag_detail.id,
                        'name' : tag_detail.name
                    } for tag_detail in tag.tagdetail_set.all()]
                } for tag in filter_tags],
            'categories' : [{
                'id' : category.id,
                'name' : category.name
            } for category in JobCategory.objects.all()]
        }

        return JsonResponse({'message':'SUCCESS', 'data':data}, status=200)

class PostingDetailView(View):
    @non_user_accept_decorator
    def get(self, request, posting_id):
        """[Posting] 채용공고 상세 페이지
        Args:
            - posting_id : path parameter로 들어오는 채용공고 하나의 id값
        Return:
            - 200: {'message' : 'SUCCESS', 'data': 하나의 채용공고에 대한 상세 정보, 접속한 유저에 대한 정보}
            - 404 (존재하지 않는 채용공고입니다) : 유효하지 않은 posting 의 id로 접근했을 경우
        Note:
            - 로그인 유저일 경우 : 해당 채용공고에 "좋아요" 나 "북마크 했을 시 해당 값에 True 반환 => UI에서 이모티콘 구현
            - 비회원 유저일 경우 : 위의 값에 False로 반환
        """
        try:
            user     = request.user
            posting  = Posting.objects.get(id=posting_id)
            result   = []
            contents = {
                    'id'           : posting.id,
                    'title'        : posting.title,
                    'company'      : posting.company_detail.company.name,
                    'city'         : posting.company_detail.state.name,
                    'district'     : posting.company_detail.county.name,
                    'detailAddress': posting.company_detail.address,
                    'latitude'     : float(posting.company_detail.latitude),
                    'longitude'    : float(posting.company_detail.longitude),
                    'tags'         : [tag_detail.name for tag_detail in posting.company_detail.company.tag.all()],
                    'description'  : posting.description,
                    'image'        : posting.company_detail.company.companyimage_set.first().image_url,
                    'bonus'        : int(posting.reward),
                    'like'         : posting.like_set.count(),
                    'deadline'     : str(posting.end_date)[:10],
                    'logoSrc'      : posting.company_detail.company.icon,
                    'category'     : posting.job_category.occupation.name,
                        }
            # 비회원 유저일 경우
            if user is None:
                contents['user']         = None
                contents['userLike']     = False
                contents['userBookmark'] = False
                result.append(contents)
                return JsonResponse({'message': 'SUCCESS', 'data': result}, status=200)
            
            # 회원 유저일 경우
            contents['user']         = user.name
            contents['userLike']     = True if Like.objects.filter(user=user, posting=posting).exists() else False
            contents['userBookmark'] = True if BookMark.objects.filter(user=user, posting=posting).exists() else False
            contents['userEmail']    = user.email
            contents['userPhone']    = user.phone_number
            result.append(contents)
            return JsonResponse({'message': 'SUCCESS', 'data': result}, status=200)
            
        except Posting.DoesNotExist:
            return JsonResponse({'message': '존재하지 않는 채용공고 입니다'}, status=404) 



class RelatedPostingView(View):
    @non_user_accept_decorator
    def get(self, request, posting_id):
        """[Posting] 연관된 채용공고 목록
        Args:
            - posting_id: path parameter로 들어오는 채용공고 하나의 id값
            - page: 현재 확인하고 있는 쪽 수, query parameter로 받는 값
        Return:
            - 200: {'message' : 'SUCCESS', 'data': 하나의 채용공고에 대한 상세 정보, 접속한 유저에 대한 정보}
            - 404 (페이지 수 초과): 
            - 404 (존재하지 않는 채용공고입니다) : 유효하지 않은 posting 의 id로 접근했을 경우
        Note:
            - exclude : 선택된 메인 채용공고를 제외한 나머지 공고만 추리기 위해 사용됨.
        """
        PER_PAGE = 4
        try:
            user            = request.user
            posting         = Posting.objects.get(id=posting_id)
            posting_related = Posting.objects.filter(job_category=posting.job_category).exclude(id=posting_id).order_by('id')
            limit_page      = math.ceil(posting_related.count()/PER_PAGE)
            print("limit_page??????????", limit_page)
            page            = request.GET.get('page', 1)
            print("page?????????", page)
            paginator       = Paginator(posting_related, PER_PAGE)

            if int(page) > limit_page:
                return JsonResponse({"message": "페이지 수 초과"}, status=404)
            
            posting_related = paginator.get_page(page)
            posting_list    = [
                        {
                        'id'     : posting_related.id,
                        'image'  : posting_related.company_detail.company.companyimage_set.first().image_url,
                        'like'   : posting_related.like_set.count(),
                        'title'  : posting_related.title, 
                        'company': posting_related.company_detail.company.name,
                        'city'   : posting_related.company_detail.state.name,
                        'nation' : posting_related.company_detail.county.name,
                        'bonus'  : int(posting_related.reward),
                        'userLike' : True if Like.objects.filter(user=user, posting=posting_related).exists() else False,
                        } for posting_related in posting_related]
            return JsonResponse({'message' : 'SUCCESS', 'data': posting_list}, status=200)

        except Posting.DoesNotExist:
            return JsonResponse({'message': '존재하지 않는 채용공고입니다'}, status=404)

class PostingLikeView(View):
    @login_decorator
    def post(self, request, posting_id):
        """[Posting] 채용공고에 "좋아요" 기능 
        Args:
            - posting_id: path parameter로 들어오는 채용공고 하나의 id값
        Return:
            - 200: {'message' : 'SUCCESS', 'data': 하나의 채용공고에 대한 상세 정보, 접속한 유저에 대한 정보}
            - 404 (존재하지 않는 채용공고입니다) : 유효하지 않은 posting 의 id로 접근했을 경우
        Note:
            - 이미 로그인 유저가 "좋아요" 한 상태라면 그 관계를 삭제 (hard_delete)
        """
        try:
            user    = request.user
            
            if Like.objects.filter(user=user, posting_id=posting_id).exists():
                Like.objects.filter(user=user, posting_id=posting_id).delete()
                return JsonResponse({"message": "해당 채용공고를 좋아요 목록에서 삭제하였습니다"}, status=200)
            
            Like.objects.create(user=user, posting_id=posting_id)
            return JsonResponse({"message": "해당 채용공고를 좋아요 목록에 추가하였습니다"}, status=200)
        
        except Posting.DoesNotExist:
            return JsonResponse({'message': '존재하지 않는 채용공고입니다'}, status=404)

class PostingBookmarkView(View):
    @login_decorator
    def post(self, request, posting_id):
        """[Posting] 채용공고에 "북마크" 기능 
        Args:
            - posting_id: path parameter로 들어오는 채용공고 하나의 id값
        Return:
            - 200: {'message' : 'SUCCESS', 'data': 하나의 채용공고에 대한 상세 정보, 접속한 유저에 대한 정보}
            - 404 (존재하지 않는 채용공고입니다) : 유효하지 않은 posting 의 id로 접근했을 경우
        Note:
            - 이미 로그인 유저가 "북마크" 한 상태라면 그 관계를 삭제 (hard_delete)
        """
        try:
            user    = request.user
            
            if BookMark.objects.filter(user=user, posting=posting).exists():
                BookMark.objects.filter(user=user, posting=posting).delete()
                return JsonResponse({"message": "WASTED"}, status=200)
            
            BookMark.objects.create(user=user, posting_id=posting_id)
            return JsonResponse({"message": "SUCCESS"}, status=200)
        
        except Posting.DoesNotExist:
            return JsonResponse({'message': '존재하지 않는 채용공고입니다'}, status=404)