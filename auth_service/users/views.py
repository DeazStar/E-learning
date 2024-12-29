import json
import pika
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.mail import send_mail
from .serializers import RegisterSerializer, UserSerializer ,RequestResetPasswordSerializer, VerifyOtpAndResetPasswordSerializer


User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
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
                connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpAndResetPasswordView(APIView):
    def post(self, request):
        serializer = VerifyOtpAndResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
