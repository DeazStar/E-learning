
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    COURSE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('video', 'Video'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - Lesson {self.order}"
        
class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    questions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)