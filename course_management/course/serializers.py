
from rest_framework import serializers
from .models import Course,Enrollment, Lesson
from .models import Quiz
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'instructor', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'order', 'type', 'video_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'course', 'questions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'course_title', 'enrolled_at']