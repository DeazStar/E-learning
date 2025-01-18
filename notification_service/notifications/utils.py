from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_email(email, otp):
    """
    Sends a password reset email to the user.
    
    Args:
        email (str): The recipient's email address.
        otp (str): The otp to rest the password.
    """
    subject = "Password Reset Request"
    message = f"Hi,\n\nYou requested a password reset. Your OTP for password rest is \n\n{otp}\n\nIf you didn't request this, please ignore this email."
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

def send_prompotional_mail(email, subject, message):
    """
    Sends a password reset email to the user.
    
    Args:
        email (str): The recipient's email address.
        subject (str): mail subject
        message (str): mail message
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )