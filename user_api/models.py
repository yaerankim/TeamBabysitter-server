# from django.db import models
# # 코드 추가
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# import uuid

# # Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, emailId, password, **kwargs):
#         """
#         주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
#         """
#         if not emailId:
#             raise ValueError('Users must have an emailId address')
#         user = self.model(
#             emailId=emailId,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, emailId=None, password=None, **extra_fields):
#         """
#         주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
#         단, 최상위 사용자이므로 권한을 부여
#         """
#         superuser = self.create_user(
#             emailId=emailId,
#             password=password,
#         )
        
#         superuser.is_staff = True
#         superuser.is_superuser = True
#         superuser.is_active = True
        
#         superuser.save(using=self._db)
#         return superuser

# import json

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     # AbstractBaseUser와 PermissionsMixin을 상속받은 custom user 모델 정의
#     ############################# 필수 #############################
#     # emailId = models.EmailField(max_length=30, unique=True, null=False, blank=False)
#     emailId = models.EmailField(unique=True, max_length=30, null=False, blank=False)
#     # idToken = models.CharField(max_length=30, blank=False)
#     # idToken = models.AutoField(blank=False, primary_key=True, null=False, unique=True)
#     # idToken = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False, blank=False)
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False, blank=False)
#     password = models.CharField(max_length=30, null=False, blank=False)
#     ############################# 필수 #############################
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = UserManager()

# 	# 사용자의 username field는 email으로 설정 (이메일로 로그인)
#     USERNAME_FIELD = 'emailId'