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
        try:
            data = json.loads(request.body)

            user            = request.user
            name            = data.get('name', user.name)
            work_experience = data.get('workExperience', user.work_experience)
            salary          = data.get('salary', user.salary)
            phone_number    = data.get('phoneNumber', user.phone_number)

            user.name            = name
            user.work_experience = work_experience
            user.salary          = salary
            user.phone_number    = phone_number
            user.save()

            for skill in data.get('skills', []):
                user.skill.add(skill)
            
            for job in data.get('jobCategory', []):
                user.job_category.add(job)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        return JsonResponse({'message':'SUCCESS'}, status=201)

