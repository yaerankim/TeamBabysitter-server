from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField

from django.contrib.auth.models import BaseUserManager

# from going_baby.authentication.managers import UserManager
# from going_baby.core.models import TimestampedModel

# [참고] github >> encode/django-rest-framework/rest_framework/authtoken/models.py
# class Token(models.Model):
#     """
#     The default authorization token model.
#     """
#     key = models.CharField(_("Key"), max_length=40, primary_key=True)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name='auth_token',
#         on_delete=models.CASCADE, verbose_name=_("User")
#     )
#     created = models.DateTimeField(_("Created"), auto_now_add=True)

#     class Meta:
#         abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super().save(*args, **kwargs)

#     @classmethod
#     def generate_key(cls):
#         return binascii.hexlify(os.urandom(20)).decode()

#     def __str__(self):
#         return self.key

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, id, email, password): #, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            id=id,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            id=id,
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser

# Create your models here.
# class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
#     user_id = models.AutoField(unique=True) # BigAutoField
#     id = models.CharField(max_length=255)
#     pw = models.CharField(max_length=255)
#     username = models.CharField(max_length=255)
#     nickname = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(db_index=True, unique=True)
#     address = models.CharField(max_length=255)
#     # birthday = models.DateField() # 없어도 될 field
#     phone_number = models.CharField(max_length=255)
#     baby_gender = BooleanField(default=False) # False(남아), True(여아)
#     baby_name = models.CharField(max_length=255)
#     baby_birthday = models.DateField() # 확인 필요
#     # is_active = BooleanField(default=True) # 필요하다면 추가
#     # is_staff = BooleanField(default=False) # 필요하다면 추가
    
#     USERNAME_FIELD = 'id'
    
#     REQUIRED_FIELDS = [
#         'nickname',
#         'pw'
#     ]
    
#     objects = UserManager()
    
#     def __str__(self):
#         return self.id
    
#     def get_full_nickname(self):
#         return self.nickname

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(unique=True, primary_key=True)
    id = models.CharField(max_length=30, null=False, blank=False)
    pw = models.IntegerField(null=False, blank=False) # 수정 # 재확인 필요 # CharField
    username = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    baby_gender = BooleanField(default=False) # False(남아), True(여아)
    baby_name = models.CharField(max_length=255)
    # baby_birthday = models.DateField() # 확인 필요
    # is_superuser = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'nickname' # 수정
    REQUIRED_FIELDS = ['user_id', 'id', 'pw', 'email'] # 수정

    class Meta:
        db_table = 'user'