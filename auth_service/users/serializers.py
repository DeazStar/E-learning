from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
 
from users.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True},  # Ensure role is required
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.get('role')  # Get the role from the validated data
        instance = self.Meta.model(**validated_data)

        # Set the password securely
        if password:
            instance.set_password(password)

        # Ensure the role is properly assigned
        if role not in dict(CustomUser.ROLE_CHOICES):  # Validate role against allowed choices
            raise serializers.ValidationError({'role': 'Invalid role provided'})

        instance.save()
        return instance

class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class VerifyOtpAndResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        otp = data['otp']
        user = User.objects.filter(email=email).first()

        if not user or user.reset_otp != otp:
            raise serializers.ValidationError("Invalid OTP.")
        if user.otp_expiry < now():
            raise serializers.ValidationError("OTP has expired.")
        return data

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)  # Reset the password
        user.reset_otp = None  # Clear the OTP
        user.otp_expiry = None
        user.save()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role  # Ensure 'role' is added from the CustomUser model
        return token