# import re, bcrypt, jwt

from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from drf_extra_fields.fields import Base64ImageField, HybridImageField
# from .utils import (
#     email_isvalid, 
#     password_isvalid, 
#     nickname_isvalid,
#     hash_password,
#     check_password,
# )

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'user_image', 'nickname', 'baby_birthday', 'baby_gender']
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=User.objects.all(),
#                 fields=('email', 'nickname'),
#                 message="이미 존재하는 회원입니다."
#             ),
#         ]

#     # def validate_email(self, obj):
#     #     if email_isvalid(obj):
#     #         return obj
#     #     raise serializers.ValidationError('메일 형식이 올바르지 않습니다.')

#     # def validate_nickname(self, obj):
#     #     if nickname_isvalid(obj):
#     #         return obj
#     #     raise serializers.ValidationError('닉네임은 한 글자 이상이어야 합니다.')

#     def update(self, obj, validated_data):
#         obj.email = validated_data.get('email', obj.email)
#         obj.user_image = validated_data.get('user_image', obj.user_image)
#         obj.nickname = validated_data.get('nickname', obj.nickname)
#         obj.baby_birthday = validated_data.get('baby_birthday', obj.baby_birthday)
#         obj.baby_gender = validated_data.get('baby_gender', obj.baby_gender)
#         obj.save()
#         return obj
        
            
# class LoginSerializer(serializers.ModelSerializer):
#     access_token = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'access_token')
#         write_only_fields = ['email', 'password']
    
#     # def validate_password(self, obj):
#     #     email = self.initial_data['email']
#     #     password = User.objects.get(email=email).password
#     #     if check_password(obj, password):
#     #         return password
#     #     raise serializers.ValidationError('비밀번호가 올바르지 않습니다.')

#     def get_access_token(self, obj):
#         user = User.objects.get(id=obj.id)
#         refresh = RefreshToken.for_user(user)
#         return str(refresh.access_token)

# login이나 logout할 때의 post와 겹치는 것 같길래 Register용 시리얼라이저 따로 마련해봄(성공)
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

# user 회원가입 및 로그인 시 사용
class UserSerializer(serializers.ModelSerializer): # serializers.HyperlinkedModelSerializer
    user_image = HybridImageField(use_url=True) # default image를 file로서 인정해줌
    class Meta:
        model = User
        fields = ['email', 'password', 'user_image', 'nickname', 'baby_birthday', 'baby_gender']

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

    # register 시 keyerror: request 발생해서 주석 처리
    # 이메일 수정 관련 검증
    # def validate_email(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value

    # # 닉네임 수정 관련 검증
    # def validate_nickname(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
    #         raise serializers.ValidationError({"nickname": "This nickname is already in use."})
    #     return value

    def update(self, instance, validated_data):
        # partial=True이므로 입력되지 않은 값이 있을 경우 이전 값(instance)을 기본값으로 사용하도록 설정
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.user_image = validated_data.get('user_image', instance.user_image)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.baby_birthday = validated_data.get('baby_birthday', instance.baby_birthday)
        instance.baby_gender = validated_data.get('baby_gender', instance.baby_gender)

        # if baby_gender is not None:
        #     if baby_gender.lower() == 'true':
        #         instance.baby_gender = True
        #     elif baby_gender.lower() == 'false':
        #         instance.baby_gender = False

        instance.save()

        return instance

# # mypage에서 수정 시 사용
# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'user_image', 'nickname', 'baby_birthday', 'baby_gender']

#     # # 이메일 수정 관련 검증
#     # def validate_email(self, value):
#     #     user = self.context['request'].user
#     #     if User.objects.exclude(pk=user.pk).filter(email=value).exists():
#     #         raise serializers.ValidationError({"email": "This email is already in use."})
#     #     return value

#     # # 닉네임 수정 관련 검증
#     # def validate_nickname(self, value):
#     #     user = self.context['request'].user
#     #     if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
#     #         raise serializers.ValidationError({"nickname": "This nickname is already in use."})
#     #     return value

#     def update(self, instance, validated_data):
#         # instance.email = validated_data['email']
#         instance.user_image = validated_data['user_image']
#         instance.nickname = validated_data['nickname']
#         instance.baby_birthday = validated_data['baby_birthday']
#         instance.baby_gender = validated_data['baby_gender']

#         # if baby_gender is not None:
#         #     if baby_gender.lower() == 'true':
#         #         instance.baby_gender = True
#         #     elif baby_gender.lower() == 'false':
#         #         instance.baby_gender = False

#         instance.save()

#         return instance