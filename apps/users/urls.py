from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import UserInfoView, UserRegistrationView

schema_view = get_schema_view(
   openapi.Info(
      title="RetroPixel Studio (Users API)",
      default_version='v1',
      description="Documentación de los endpoints de la aplicación 'users'.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@miapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user_info/', UserInfoView.as_view(), name='user_info'),
    path('api/user_registration/', UserRegistrationView.as_view(), name='user_registration'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]