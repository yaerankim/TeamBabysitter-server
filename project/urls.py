"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from user_api.views import RegisterAPIView, LoginAPIView #, UpdateAPIView
# from user_api.views import Register, Login, MyPageView
from user_api.views import RegisterView, LoginView, LogoutView, UserView
from community.views import CommunityCreate, CommunityDetail, CommunityList, CommentCreate, CommentDetail

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("user/register/", RegisterAPIView.as_view()), # 1
    # path("user/login/", LoginAPIView.as_view()), # 1
    # path("user/register/", Register.as_view()), # 2
    # path("user/login/", Login.as_view()), # 2
    # path('user/mypage/', MyPageView.as_view()), # 2
    # path("user/update/", UpdateAPIView.as_view()), # 1
    # path("user/auth/refresh/", TokenRefreshView.as_view()), # 0
    path("user/register/", RegisterView.as_view()),
    path("user/login/", LoginView.as_view()),
    path("user/logout/", LogoutView.as_view()),
    path("user/view/", UserView.as_view()),
    path('community/create/', CommunityCreate.as_view(), name='community-create'),
    path('community/<int:pk>', CommunityDetail.as_view(), name='community-detail'),
    path('community/', CommunityList.as_view(), name='community-list'),
    path('comment/create/<int:pk>', CommentCreate.as_view(), name='comment-create'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment-detail'),
    # path('login/', login, name='login'),
    # path('login/', AuthAPIView.as_view()),
    # path('list/', ListUsers.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
