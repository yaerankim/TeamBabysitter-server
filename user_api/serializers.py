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
        # partial=True이므로 입력되지 않은 값이 있을 경우 이전 값(instance)을 기본값으로 사용하도록 설정
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
    user_image = serializers.ImageField(use_url=True) # 이미지의 url을 직렬화하여 반환하도록 함

    class Meta:
        model = User
        fields = ['id', 'email', 'user_image', 'nickname', 'baby_birthday', 'baby_gender'] # id 추가

    # def get(self, obj):
    #     # 임의로 작성한 코드
    #     obj.nickname = User.objects.get(id=obj.id).nickname
    #     obj.baby_birthday = User.objects.get(id=obj.id).baby_birthday
    #     obj.baby_gender = User.objects.get(id=obj.id).baby_gender
    #     return obj