from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_email(email, reset_link):
    """
    Sends a password reset email to the user.
    
    Args:
        email (str): The recipient's email address.
        reset_link (str): The password reset link.
    """
    subject = "Password Reset Request"
    message = f"Hi,\n\nYou requested a password reset. Click the link below to reset your password:\n\n{reset_link}\n\nIf you didn't request this, please ignore this email."
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
