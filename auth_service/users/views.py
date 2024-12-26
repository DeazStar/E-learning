from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.mail import send_mail
from .serializers import RegisterSerializer, UserSerializer ,RequestResetPasswordSerializer, VerifyOtpAndResetPasswordSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


User = get_user_model()



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save user and handle role assignment
            user = serializer.save()

            # Ensure the role is included and valid
            if not user.role:
                return Response({'error': 'Role is required'}, status=400)

            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)

class RoleBasedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'student' or request.user.role == 'instructor':
            return Response(
                {'id': request.user.id,
                 'role': request.user.role,
                 }
                
                )
        
        return Response({'message': 'Role not found'}, status=403)


class RequestResetPasswordView(APIView):
    def post(self, request):
        serializer = RequestResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            user.generate_otp()  # Generate and save the OTP

            # Send OTP via email
            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP for password reset is {user.reset_otp}",
                from_email="no-reply@example.com",
                recipient_list=[email],
            )

            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpAndResetPasswordView(APIView):
    def post(self, request):
        serializer = VerifyOtpAndResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token', None)

        if not token:
            return Response({"error": "Token is required."}, status=400)

        try:
            decoded_token = UntypedToken(token)
            user_id = decoded_token.get('user_id')
            role = decoded_token.get('role', None)  # Ensure role is explicitly fetched

            # Debugging
            print(f"Decoded Token Payload: {decoded_token}")

            return Response({
                "valid": True,
                "user_id": user_id,
                "role": role if role else "Role not found in token"
            }, status=200)
        except Exception as e:
            raise AuthenticationFailed("Invalid or expired token.") from e

