from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, email_verification, UserListView, UserBanView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registr/', RegisterView.as_view(), name='register'),
    path('confirm/<str:token>/', email_verification, name='email_verification'),
    path('all/', UserListView.as_view(), name='list_users'),
    path('ban/<int:pk>', UserBanView.as_view(), name='ban_user'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile_user'),
]
