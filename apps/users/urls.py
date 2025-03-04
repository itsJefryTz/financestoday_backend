from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserInfoView, UserRegistrationView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user_info/', UserInfoView.as_view(), name='user_info'),
    path('api/user_registration/', UserRegistrationView.as_view(), name='user_registration'),
]