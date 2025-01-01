import os
import environ
import requests
from django.http import JsonResponse
from django.views import View
from gateway.middleware import authentication_required 

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Explicitly point to the .env file
ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
environ.Env.read_env(ENV_FILE)

# Get the service URLs using django-environ
COURSE_SERVICE_URL = env("COURSE_SERVICE_URL")
AUTH_SERVICE_URL = env("AUTH_SERVICE_URL")

class CourseServiceProxyView(View):
    @authentication_required
    def get(self, request, *args, **kwargs):
        headers = {"X-User-ID": request.user_id, "Authorization": request.headers.get("Authorization")}
        try:
            response = requests.get(f"{COURSE_SERVICE_URL}/api/courses/", headers=headers)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException:
            return JsonResponse({"error": "Course service is unavailable"}, status=503)
        
class AuthServiceProxyView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Forward headers and body from the incoming request
            headers = {"Authorization": request.headers.get("Authorization")}
            response = requests.post(
                f"{AUTH_SERVICE_URL}/api/user/",
                json=request.POST.dict() or {},  # Forward POST data as JSON
                headers=headers
            )
            return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException:
            return JsonResponse({"error": "Authentication service is unavailable"}, status=503)