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
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        # 기존 코드
        res = Response()
        res.delete_cookie('jwt')
        res.data = {
            "message" : 'success'
        }
        return res

# 로그인 유지(로그인 여부 확인)
class UserView(APIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get(self,req):
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        user = User.objects.get(id=payload['id'])
        
        serializer = UserDetailSerializer(user)

        return Response(serializer.data)

    # account 수정 시
    def put(self,req): # pk 추가
        token = req.COOKIES.get('jwt')

        if not token :
            raise AuthenticationFailed('UnAuthenticated!')

        try :
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')

        user = User.objects.get(id=payload['id'])
        serializer = UserDetailSerializer(user, data=req.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)