import environ
import os

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Explicitly point to the .env file
ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
environ.Env.read_env(ENV_FILE)

# Email Configuration
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT', default=2525)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='no-reply@gmail.com')


# Allowed hosts
ALLOWED_HOSTS = ['*']  # Allow all hosts (use only in development)

# Installed apps configuration

INSTALLED_APPS = [
    'notifications.apps.NotificationsConfig',
]
