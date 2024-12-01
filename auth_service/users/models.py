# from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    reset_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        import random
        self.reset_otp = f"{random.randint(100000, 999999)}"  # Generate a 6-digit OTP
        self.otp_expiry = now() + timedelta(minutes=10)  # OTP valid for 10 minutes
        self.save()

