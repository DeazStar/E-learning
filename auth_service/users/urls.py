from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterView, RoleBasedView , RequestResetPasswordView , VerifyOtpAndResetPasswordView,VerifyTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_me/', RoleBasedView.as_view(), name='role_based'),
    path('password-reset/request/', RequestResetPasswordView.as_view(), name='password_reset_request'),
    path('password-reset/verify/', VerifyOtpAndResetPasswordView.as_view(), name='password_reset_verify'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),

]

