# import re, json, bcrypt, jwt

from django.views import View
# from rest_framework.views import APIView
from rest_framework.decorators import APIView
from rest_framework.renderers import JSONRenderer
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import jwt, datetime
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
# from watti_backend.settings import SECRET_KEY
from django.conf import settings
from .models import User
# from .utils import login_decorator
from rest_framework.exceptions import AuthenticationFailed

from django.core.files.storage import FileSystemStorage

# 역시나 로그인 유지X.
# class Register(APIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(data=serializer.data, status=200)
#         return Response(data="INFO_INVALID", status=400)

#     @login_decorator
#     def patch(self, request):
#         serializer_class = UserSerializer
#         user = User.objects.get(id=request.user.id)
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(data=serializer.data, status=200)
#         return Response(data='INFO_INVALID', status=400)

# class Login(APIView):
#     queryset = User.objects.all()
#     serializer_class = LoginSerializer
#     def post(self, request):
#         try:
#             user = User.objects.get(email=request.data['email'])
#             serializer = LoginSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid(raise_exception=True):
#                 return Response(data=serializer.data, status=200)
#             return Response(data='INVALID_LOGIN_INFO', status=400)
        
#         except User.DoesNotExist:
#             return Response(data='사용자가 존재하지 않습니다.', status=400)

# class MyPageView(View):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     @login_decorator
#     def get(self, request):
#         try:
#             user = User.objects.get(id=request.user.id)
            
#             context = {
#                 'user_image': user.user_image,
#                 'nickname': user.nickname,
#                 'baby_birthday': user.baby_birthday,
#                 'baby_gender': user.baby_gender,
#             }
#             return JsonResponse({'context': context}, status=200)

#         except User.DoesNotExist:
#             return JsonResponse({'message': 'DOES_NOT_EXIST', 'error_message': '해당 사용자는 존재하지 않습니다.'})
#         except KeyError:
#             return JsonResponse({'message':'KEY_ERROR'}, status=400)

# 처음에 시도한 방식
# 로그인 유지X. udpate 하면 모든 레코드가 동일하게 수정됨.
# class RegisterAPIView(APIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.save()

#             # 두 번 지정하게 되므로 IntegrityError 발생 SO 주석 처리
#             # user = User.objects.create(
#             #         email = request.data['email'],
#             #         password = request.data['password'],
#             # )

#             # user_image의 값으로 사진을 업로드하면 지정 폴더 안에 이미지 저장(실패)
#             # if request.FILES["user_image"]:
#             #     uploaded_user_image = request.FILES["user_image"]
#             #     fs = FileSystemStorage(
#             #         location="media/user", base_url="/media/user"
#             #     )
#             #     filename = fs.save(uploaded_user_image.name, uploaded_user_image)
#             #     uploaded_user_image_url = fs.url(filename)

#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)

#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
            
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
            
#             return res
#             # return Response(serializer.data + res, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginAPIView(APIView):
#     queryset= User.objects.all()
#     serializer_class= UserSerializer
#     # permission_classes = [IsAuthenticated]
#     # 로그인
#     def post(self, request):
#         # permission_classes = [AllowAny]
#     	# 유저 인증
#         user = authenticate(
#             email=request.data.get("email"), password=request.data.get("password")
#         )
#         # 이미 회원가입 된 유저일 때
#         if user is not None:
#             serializer = UserSerializer(user)
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
#             return res
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그아웃
#     # @login_required -> CBV에서는 사용 불가
#     def delete(self, request):
#         # permission_classes = [IsAuthenticated]
#         if not request.user.is_authenticated:
#             return redirect("user/login/")
#         res = Response(
#             {
#                 "message": "Logout success"
#             },
#             status=status.HTTP_200_OK,
#             # status=status.HTTP_202_ACCEPTED, # 비동기
#         )

#         # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
#         res.delete_cookie("access")
#         res.delete_cookie("refresh")

#         return res

#     # account 변경
#     def put(self, request):
#         # User = get_user_model()
#         # permission_classes = [IsAuthenticated]
#         user = User.objects.update(
#             # email = request.data['email'],
#             user_image = request.data['user_image'],
#             nickname = request.data['nickname'],
#             baby_birthday = request.data['baby_birthday'],
#             baby_gender = request.data['baby_gender'],
#         )
#         res = Response(
#             # {
#             #     "user": user.data,
#             # },
#             status=status.HTTP_200_OK,
#         )
#         return res

# # account 변경
# 이렇게 따로 둔 상태로 permission이 IsAuthenticated이면
# 로그인을 해도 로그인을 안 한 걸로 간주함
# SO 로그인 APIView 안에 수정 메서드를 같이 둬야 함
# class UpdateAPIView(APIView):
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class= UserSerializer

#     def put(self, request):
#         permission_classes = [IsAuthenticated]
#         user = User.objects.update(
#             email = request.data['email'],
#             user_image = request.data['user_image'],
#             nickname = request.data['nickname'],
#             baby_birthday = request.data['baby_birthday'],
#             baby_gender = request.data['baby_gender'],
#         )

# # account 변경
# class UpdateAPIView(generics.UpdateAPIView):
#     model = User
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserUpdateSerializer

#     def put(self, request):
#         user = User.objects.update(
#             # email = request.data['email'],
#             user_image = request.data['user_image'],
#             nickname = request.data['nickname'],
#             baby_birthday = request.data['baby_birthday'],
#             baby_gender = request.data['baby_gender'],
#         )
#         res = Response(
#             # {
#             #     "user": user.data,
#             # },
#             status=status.HTTP_200_OK,
#         )
#         return res

# 회원가입
class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    def post(self, req):
        serializer = UserRegisterSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

# 로그인
class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self,req):
        email = req.data['email']
        password = req.data['password']

        # email is unique,
        user = User.objects.filter(email=email).first()
        serialize_user = UserSerializer(user)
        json_user = JSONRenderer().render(serialize_user.data)

        if user is None :
            raise AuthenticationFailed('User does not found!')

        # is same?
        if not user.check_password(password) :
            raise AuthenticationFailed("Incorrect password!")

        ## JWT 구현 부분
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256").decode("utf-8")

        res = Response()
        res.set_cookie(key='jwt', value=token, httponly=True)
        res.data = {
            'jwt' : token
        }
        return res

# 로그아웃
class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self,req):
        res = Response()
        res.delete_cookie('jwt')
        res.data = {
            "message" : 'success'
        }
        return res

# 로그인 유지(로그인 여부 확인)
class UserView(APIView):
    # permission_classes = [IsAuthenticated] # 이걸 굳이 설정하지 않더라도 로그아웃 후에는 해당 계정에 대한 get이 안되긴 함
    def get(self,req):
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

    # account 수정 시
    def put(self,req):
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        # data=req.data를 추가하여 serializer의 update() 호출
        # partial=True로 설정하여 put 중에서도 일부만 수정해도 문제 없도록 설정
        serializer = UserSerializer(user, data=req.data, partial=True)

        if serializer.is_valid():
            serializer.save() # 데이터 저장

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        