from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import CustomUser
import firebase_admin
from firebase_admin import auth
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from firebase_authentication.authentication import FirebaseAuthentication, verify_user_token
from firebase_admin import db
from rest_framework_simplejwt.authentication import JWTAuthentication
import json

from django.core.serializers.json import DjangoJSONEncoder # json.dumps() 사용 가능.

from firebase_admin import credentials

from django.contrib.auth import get_user_model
from django.conf import settings

UserModel = get_user_model()
cred = firebase_admin.credentials.Certificate(settings.FIREBASE_PATH)
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://fir-emailaccount-fa39e-default-rtdb.firebaseio.com/'
})

# 회원가입
# 회원가입 기능 구현은 일단 simplejwt 사용방식과 동일하게 하기
# 회원가입하면 firebase DB에도 저장되도록 하기 -> firebase_admin의 db 사용
@api_view(['POST'])
# @authentication_classes([FirebaseAuthentication])
# @authentication_classes([JWTAuthentication, FirebaseAuthentication])
# @permission_classes([AllowAny])
def register(request):
    # # 프론트엔드로부터 사용자의 입력 정보 받기
    # emailId = request.data.get('emailId')
    # # id = request.data.get('id')
    # password = request.data.get('password')

    # # create user
    # # firebase DB에는 저장된 상태이므로 auth.sign_in... 할 필요X.
    # # Django DB에 사용자 필수 입력 정보 저장
    # user = CustomUser.objects.create_user(
    #     emailId=emailId,
    #     # id=id,
    #     password=password,
    # )

    # return Response({'message': 'User created successfully'})
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # jwt 토큰 접근
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "message": "register successs",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        
        # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)

        dir = db.reference('GoingBaby/UserAccount/%s' % str(user.id))
        dir.update({'emailId':user.emailId})
        dir.update({'idToken':json.dumps(user.id, cls=DjangoJSONEncoder)})
        dir.update({'password':user.password})

        return res
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthAPIView(APIView):
    # permission_classes = [AllowAny] # 로그인 여부 확인하는 클래스 지정
    # authentication_classes = [FirebaseAuthentication, JWTAuthentication] # 로그인과 관련된 기능 수행을 위한 클래스 지정
    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    @csrf_exempt
    # 로그인
    # firebase DB에 저장된 모든 회원가입 정보들 먼저 가져오기
    # 해당 내용과 일치하면 로그인 성공
    def post(self, request):
        # 프론트엔드로부터 사용자의 로그인 정보 전달받아 사용자 인증하기
        user = authenticate(
            emailId=request.data.get("emailId"), password=request.data.get("password")
        )
        # 등록된 사용자라면
        if user is not None:
            serializer = UserSerializer(user)
            id = request.data.get('id')
            decoded_token = auth.verify_id_token(id)
            # decoded_token = verify_user_token(id)
            id = decoded_token['id']
            user = authenticate(request)
            # refresh token과 access token 발급(simplejwt 사용)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        else:
            # 등록되지 않은 사용자라면
            return Response(status=status.HTTP_400_BAD_REQUEST)

# import pyrebase5
# from django.contrib import auth
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .serializers import *
#
# config = {
#     'apiKey': "AIzaSyCRS7Ew-pXXtcqre12pUKnBbKsodzZoNO8",
#     'authDomain': "fir-emailaccount-fa39e.firebaseapp.com",
#     'projectId': "fir-emailaccount-fa39e",
#     'storageBucket': "fir-emailaccount-fa39e.appspot.com",
#     'messagingSenderId': "1077500447473",
#     'appId': "1:1077500447473:android:0f656d7cde3e01723bb750",
#     # 'measurementId': "project-1077500447473", # 없어도 되는 듯. 확실한 값 아니기도 하고.
#     "databaseURL" : "https://fir-emailaccount-fa39e-default-rtdb.firebaseio.com/"
# }
#
# firebase = pyrebase5.initialize_app(config)
# authentication = firebase.auth() # for login logout
# database = firebase.database()
