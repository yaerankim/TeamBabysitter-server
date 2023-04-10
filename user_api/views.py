from django.shortcuts import render
import firebase_admin
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from authentication import FirebaseAuthentication

# 회원가입
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                },
                status=status.HTTP_200_OK,
            )
            # auth = firebase.auth()
            auth = FirebaseAuthentication.authenticate()
            auth.create_user_with_email_and_password(email, password)

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
