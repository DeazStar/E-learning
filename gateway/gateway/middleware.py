# middleware.py
import environ
import requests
from django.http import JsonResponse
from functools import wraps
from django.http import JsonResponse

# Initialize environment variables
env = environ.Env()

# Get the service URLs using django-environ
AUTH_SERVICE_URL = env("AUTH_SERVICE_URL")

def authentication_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authorization token is missing or invalid"}, status=401)

        token = auth_header.split(" ")[1]

        # Call Auth Service to validate the token
        try:
            response = requests.post(f"{AUTH_SERVICE_URL}/api/users/validate_token/", json={"token": token})
            if response.status_code != 200:
                return JsonResponse({"error": "Invalid token"}, status=401)

            # Attach user ID to the request for downstream services
            request.user_id = response.json().get("user_id")
        except requests.exceptions.RequestException:
            return JsonResponse({"error": "Auth service is unavailable"}, status=503)

        return view_func(request, *args, **kwargs)

    return wrapped_view

