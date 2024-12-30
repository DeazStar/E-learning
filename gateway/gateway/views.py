import environ
import requests
from django.http import JsonResponse
from django.views import View
from middleware import authentication_required 

# Initialize environment variables
env = environ.Env()

# Get the service URLs using django-environ
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
