from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from drf_extra_fields.fields import Base64ImageField, HybridImageField

# 회원가입용 시리얼라이저
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

# 로그인, 로그아웃용 시리얼라이저
class UserSerializer(serializers.ModelSerializer): # serializers.HyperlinkedModelSerializer
    user_image = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        # id, cookie 추가
        fields = ['id', 'email', 'password', 'user_image', 'nickname', 'baby_birthday', 'baby_gender']

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.user_image = validated_data.get('user_image', instance.user_image)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.baby_birthday = validated_data.get('baby_birthday', instance.baby_birthday)
        instance.baby_gender = validated_data.get('baby_gender', instance.baby_gender)

        instance.save()

        return instance

# 계정 확인용 시리얼라이저
class UserDetailSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(use_url=True) # 이미지의 url을 직렬화하여 반환

    class Meta:
        model = User
        fields = ['id', 'email', 'user_image', 'nickname', 'baby_birthday', 'baby_gender'] # id 추가