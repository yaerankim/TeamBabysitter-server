from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        id = validated_data.get('id')
        email = validated_data.get('email')
        pw = validated_data.get('pw')
        nickname = validated_data.get('nickname')
        user = User(
            id=id,
            email=email,
            pw=pw,
            nickname=nickname
        )
        user.password(pw)
        user.save()
        return user