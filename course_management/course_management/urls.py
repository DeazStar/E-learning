"""
URL configuration for course_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from course.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/course/', CourseView.as_view(), name='course'),
    path('api/course/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('api/course/lessons/', LessonView.as_view(), name='create_lesson'),
    path('api/course/lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('api/course/enroll/', EnrollView.as_view(), name='enroll'),
    path('api/course/enrolled-courses/', EnrolledCoursesView.as_view(), name='enrolled-courses'),

    path('api/course/quizzes/', QuizView.as_view(), name='quiz'),  # List and create quizzes
    path('api/course/quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz_detail'),  # Delete a specific quiz by ID
]
