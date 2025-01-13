from django.urls import path
from .views import google_auth, google_auth_mobile


urlpatterns = [
    path('api/auth/google/', google_auth, name='google-auth'), # Web Popup flow
    path('api/auth/google/mobile/', google_auth_mobile, name='google-auth-mobile'), # Mobile app
]