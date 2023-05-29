from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    # ------------------------------- 필드 -------------------------------
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # mypage 구성할 필드들(필수X)
    # CharField와 TextField -> null=True 와 blank=True 를 동시에 사용X. blank=True만 적용 권장.
    user_image = models.ImageField(upload_to='user/', default='user/default_image.png', blank=True) # user 프로필 사진
    # user_image = models.FileField(upload_to='user/', default='user/default_image.png', blank=True)
    nickname = models.CharField(max_length=30, blank=True) # user가 커뮤니티 등에서 사용할 닉네임
    baby_birthday = models.CharField(max_length=6, blank=True) # YYMMDD
    # baby_gender = models.BooleanField(default=False) # 남아(0), 여아(1) # 계속 ValidationError 발생 -> '“true” value must be either True or False.'
    baby_gender = models.CharField(max_length=1, blank=True) # 남아(m), 여아(f)
    # ------------------------------- 필드 -------------------------------

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = 'email'