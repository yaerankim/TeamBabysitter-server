from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from firebase_authentication.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
# from .models import CustomUser
from firebase_authentication.models import User # 추가
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

# UserModel = get_user_model()
# cred = firebase_admin.credentials.Certificate(settings.FIREBASE_PATH)
# firebase_app = firebase_admin.initialize_app(cred, {
#     'databaseURL' : 'https://fir-emailaccount-fa39e-default-rtdb.firebaseio.com/'
# })

# 회원가입
@api_view(['POST'])
def register(request):
    # firebase authentication에 사용자 생성하여 등록
    serializer = UserSerializer.create(request.data) # create가 UserManager의 create_user()로 이어짐.
    if serializer.is_valid():
        user = serializer.save()
        
        res = Response(
            {
                "user": serializer.data,
                "message": "register successs",
            },
            status=status.HTTP_200_OK,
        )
        return res
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @api_view(['POST'])
    @csrf_exempt
    def post(self, request):
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
