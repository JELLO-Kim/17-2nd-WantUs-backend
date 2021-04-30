# ⚒ Team WantUs
> 구인 구직 사이트인 '원티드'를 모티브로 하여 기능을 구현한 팀 프로젝트 입니다.

👇 아래 이미지를 클릭하시면 시연 영상이 재생됩니다.
[![WantUs](https://media.vlpt.us/images/c_hyun403/post/c8542eea-b590-407b-bb7d-ff90485dc73f/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-04-27%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2011.34.21.png)](https://youtu.be/a_ufo5CdTQs)
- 진행기간 : 2021년 3월 2일 ~ 2021년 3월 12일

<br>

## ⛑ team members
프론트엔드 : 3명
<br>
**백엔드 : 3명**

<br>
<br>

# 🌈 프로젝트 소개
> **원티드?** <br> 원티드는 **기업과 구직자 모두가 이용하는 사이트로 채용정보와 함께 다양한 직군별 정보를 제공합니다.**
<br>

> **Goals : 하나의 cycle 완성하기**
<br> 유저의 회원가입/로그인 -> 채용 공고 탐색 -> 이력서 작성하기 -> 구직활동하기 (채용공고에 지원하기) -> 지원현황 확인하기&북마크 게시물 확인하기

<br>
<br>

# 🛠 기술 스택
- Lagnague : Python 3
- Framework : Django
- Modeling : AQueryTool
- Database : MySQL
- 인증, 인가 : Bcrypt, JWT
- Social Login : KakaoTalk API
- test : Django의 python 상속 unit test
- AWS : RDS, S3

<br>
<br>

# 👩🏻‍💻 구현 기능

## BackEnd (담당한 기능)

- KakaoTal Login API를 이용한 소셜 회원가입&로그인 API 구현
- Bcrypt와 JWT를 통해 비밀번호 암호화와 토큰 발행
- 회원 유효성 판단(login_decorator) 함수 작성
- 비회원 허용 유효성 판단 (non_user_accept_decorator) 함수 작성
- python에서 제공하는 Pagination 기능을 통해 채용 list의 pagination 구현
- 로그인 user의 사이트 기본 제공 양식 이력서 생성과 삭제 API 구현
- 마이페이지 : 로그인 user의 지원 현황 확인 API 구현
- 마이페이지 : 로그인 user의 "좋아요"와 "북마크"한 채용공고 내용 반환 API 구현
- Django환경에서 unit test 구현

<br>
<br>

# Project 구조
```python
.
├── __pycache__
│   ├── my_settings.cpython-38.pyc
│   ├── my_settings.cpython-39.pyc
│   └── utils.cpython-39.pyc
├── apply
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   ├── tests.cpython-39.pyc
│   │   ├── urls.cpython-39.pyc
│   │   └── views.cpython-39.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20210310_1648.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-39.pyc
│   │       ├── 0002_auto_20210303_1856.cpython-39.pyc
│   │       ├── 0002_auto_20210304_1641.cpython-39.pyc
│   │       ├── 0002_auto_20210305_1352.cpython-39.pyc
│   │       ├── 0002_auto_20210310_1648.cpython-39.pyc
│   │       ├── 0003_auto_20210310_0331.cpython-39.pyc
│   │       └── __init__.cpython-39.pyc
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── my_settings.py
├── posting
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   ├── tests.cpython-39.pyc
│   │   ├── urls.cpython-39.pyc
│   │   └── views.cpython-39.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20210310_1648.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-39.pyc
│   │       ├── 0002_auto_20210303_1856.cpython-39.pyc
│   │       ├── 0002_auto_20210304_1641.cpython-39.pyc
│   │       ├── 0002_auto_20210305_1352.cpython-39.pyc
│   │       ├── 0002_auto_20210310_1648.cpython-39.pyc
│   │       ├── 0003_auto_20210304_1547.cpython-39.pyc
│   │       ├── 0003_auto_20210304_2340.cpython-39.pyc
│   │       ├── 0003_posting_work_experience.cpython-39.pyc
│   │       ├── 0004_auto_20210304_1816.cpython-39.pyc
│   │       ├── 0004_auto_20210304_2358.cpython-39.pyc
│   │       └── __init__.cpython-39.pyc
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── pull_request_template.md
├── requirements.txt
├── resume
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   ├── tests.cpython-39.pyc
│   │   ├── urls.cpython-39.pyc
│   │   └── views.cpython-39.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-39.pyc
│   │       ├── 0002_auto_20210304_1547.cpython-39.pyc
│   │       ├── 0002_auto_20210307_1329.cpython-39.pyc
│   │       ├── 0003_auto_20210307_1330.cpython-39.pyc
│   │       ├── 0004_auto_20210310_0403.cpython-39.pyc
│   │       ├── 0004_resumefile_uuidcode.cpython-39.pyc
│   │       ├── 0005_auto_20210310_1019.cpython-39.pyc
│   │       ├── 0006_merge_20210310_1223.cpython-39.pyc
│   │       ├── 0007_resumefile_is_default.cpython-39.pyc
│   │       └── __init__.cpython-39.pyc
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── user
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   ├── tests.cpython-39.pyc
│   │   ├── urls.cpython-39.pyc
│   │   └── views.cpython-39.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-39.pyc
│   │       ├── 0002_auto_20210303_1909.cpython-39.pyc
│   │       ├── 0003_auto_20210304_1547.cpython-39.pyc
│   │       └── __init__.cpython-39.pyc
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── utils.py
└── wantus
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   ├── __init__.cpython-39.pyc
    │   ├── settings.cpython-38.pyc
    │   ├── settings.cpython-39.pyc
    │   ├── urls.cpython-39.pyc
    │   └── wsgi.cpython-39.pyc
    ├── asgi.py
    ├── asset_storage.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

# ✅ 기능 구현 상세 ✅

## 1. modeling
기존의 `원티드`사이트에서는 채용공고와 해당 회사에 대한 여러 카테고리가 존재합니다. 때문에 카테고리별 검색 혹은 필터링을 위해 이 부분을 살려 `정규화` 하였습니다.

## 2. Kakao Login API
이번 프로젝트에서는 실제 카카오 로그인 API를 사용해 소셜 로그인이 가능하도록 구현하였습니다. 유저가 입력한 카카오의 로그인 정보로 클라이언트에서 카카오API와 통신하여 카카오에서 발급하는 access_token을 받아 서버에 전달해 줍니다.
전달된 token으로 서버에서는 kakao와 통신하여 그 속에 존재하는 유저에 대한 정보 중 프로젝트상황에 맞는 정보만을 받아 해당 정보를 토대로 회원가입을 진행합니다.
만약 이미 database에 저장된 유저인 경우 회원가입되지 않고 바로 로그인이 진행되어 서버에서 발급해주는 access_token이 클라이언트에 전달됩니다.

## 3. 로그인 유저의 메인 페이지
로그인 유저가 접근시 보여지는 메인 페이지에는 조건에 따른 채용공고와, 채용공고를 내는 회사의 목록이 보입니다. 최신순과 북마크 순으로 나누어 조건별로 데이터를 가져온 후 갯수에 맞춰 반환하였습니다.

## 4. 이력서 생성, 수정, 삭제 기능 구현
- 이력서 생성시 사이트에서 제공해주는 기본 양식의 이력서가 생성됩니다. db에 저장된 유저의 유효한 이력서 갯수를 세어 새로운 이력서가 생성될때마다 이력서에 번호를 매겨주었습니다.
- 하나의 이력서 상세 페이지접속시 학력과 경력, 언어능력에 대한 정보를 입력할 수 있습니다. 상태에 변화가 있는 데이터값이 있는 경우 해당 데이터를 클라이언트로부터 받아 db에 update 시켜주도록 하였습니다.
- hard_delete로 이력서 삭제기능을 구현하였습니다.

## 5. 마이페이지 : 지원 현황 확인
- 지원완료/서류통과/불합격/최종합격 에 대한 4가지 step으로 지원자의 지원현황이 확인되도록 구현하였습니다.
- 유저가 "좋아요" 혹은 "북마크"한 채용공고에 대한 정보를 반환합니다. 이때 "북마크"한 채용공고일 경우 "좋아요"한 채용공고보다 더 상세한 정보들을 반환하여 보여줍니다.

## 6. Unit test
- Python으로 부터 상속받은 Django의 unit test를 통해 작성한 로직을 test하였습니다.
