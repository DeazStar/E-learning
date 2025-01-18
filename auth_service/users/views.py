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
import pika
import json


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

            try:
                
                message = {
                    "email": request.data.get("email", None),
                    "subject": "Welcome to E-learning",
                    "message": "Thank you for registering with E-learning platform. Get ready to explore, learn, and grow."
                }
            
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                channel = connection.channel()

                # Ensure the queue exists
                channel.queue_declare(queue='email')

                # Publish the message to the queue
                channel.basic_publish(
                    exchange='',
                    routing_key='email',
                    body=json.dumps(message)
                )
                connection.close()
            except Exception as e:
                print(e)

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

            otp = user.reset_otp

            # Prepare the message to send to the notification service
            message = {
                'email': email,
                'otp': otp
            }

            # Connect to RabbitMQ and send the message
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                channel = connection.channel()

                # Ensure the queue exists
                channel.queue_declare(queue='password_reset')

                # Publish the message to the queue
                channel.basic_publish(
                    exchange='',
                    routing_key='password_reset',
                    body=json.dumps(message)
                )
                connection.close()
                return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"message": f"Error sending OTP to notification service: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




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
        headers = request.data.get('headers', None)
        if not headers:
            return Response({"error": "Headers is required."}, status=400)
        
        token = headers.get('authorization', None).split(' ')[1]

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
