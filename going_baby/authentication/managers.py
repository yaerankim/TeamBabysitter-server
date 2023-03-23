from django.contrib.auth.models import BaseUserManager

# User model의 뼈대
# [참고] https://axce.tistory.com/99
class UserManager(BaseUserManager):

    # All user
    def create_user(self, id, password=None, **extra_fields):
    
        if id is None:
            raise TypeError('Users must have a id.')

        if password is None:
            raise TypeError('Users must have a password.')
    
        user = self.model(id = id)

        # django 에서 제공하는 password 설정 함수
        user.set_password(password)
        user.save()
        
        return user

    # admin user
    def create_superuser(self, id, password, **extra_fields):
        
        if password is None:
            raise TypeError('Superuser must have a password.')
        
        # "create_user"함수를 이용해 우선 사용자를 DB에 저장
        user = self.create_user(id, password, **extra_fields)
        # 관리자로 지정
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user