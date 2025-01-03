from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Quiz, Enrollment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer
from django.contrib.auth.models import User

class CreateCourseView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()  # Query all courses from the database
        serializer = CourseSerializer(courses, many=True)  # Serialize the queryset
        return Response(serializer.data, status=200)  # Return serialized data

    def post(self, request):
        data = request.data
        # data['instructor'] = request.user.id  # Automatically assign the instructor to the authenticated user
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateLessonView(APIView):
    # permission_classes = [IsAuthenticated] # /course/:id / /course?user_id=ll

    def get(self, request):
        lessons = Lesson.objects.all()  # Query all lessons from the database
        serializer = LessonSerializer(lessons, many=True)  # Serialize the queryset
        return Response(serializer.data, status=200)  # Return serialized data

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EnrollView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        course_id = request.data.get('course_id')

        # Validate user ID
        if not user_id or not course_id:
            raise ValidationError({"error": "Both 'user_id' and 'course_id' are required"})

        try:
            student = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response({"error": "User is already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

        # Create enrollment
        # enrollment = Enrollment.objects.create(student=student, course=course)
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
            course_title=course.title  # Explicitly set course title
        )
        
        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)


class EnrolledCoursesView(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')
        # Validate user ID
        if not user_id:
            raise ValidationError({"error": " 'user_id' is required"})

        student = User.objects.get(id=user_id)
        enrollments = Enrollment.objects.filter(student=student)
        courses = [enrollment.course for enrollment in enrollments]
        serialized_courses = CourseSerializer(courses, many=True)
        return Response(serialized_courses.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz
from .serializers import QuizSerializer

class CreateQuizView(APIView):
    # permission_classes = [IsAuthenticated]  # Uncomment if you need authentication

    def get(self, request):
        # Query all quizzes from the database
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
        # Log the errors for debugging
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteQuizView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request,quiz_id=None):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=200)

    def delete(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            quiz.delete()
            return Response({"detail": "Quiz deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)


# Delete Course
class DeleteCourseView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, course_id=None):
        # This GET method should not require a course_id in the URL
        # For the list of courses, you don't need a course_id
        courses = Course.objects.all()  # Query all courses from the database
        serializer = CourseSerializer(courses, many=True)  # Serialize the queryset
        return Response(serializer.data, status=200)  # Return serialized data

    def delete(self, request, course_id):
        # This method should handle course deletion
        try:
            courses = Course.objects.filter(id=course_id)  # Filter courses with the given course_id
            if not courses.exists():
                return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

            courses.delete()  # Delete the filtered courses
            Quiz.objects.filter(course=course_id).delete()  # Delete quizzes associated with the course
            Lesson.objects.filter(course=course_id).delete()  # Delete lessons associated with the course
            return Response({"detail": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete Lesson
class DeleteLessonView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, lesson_id=None):
        lessons = Lesson.objects.all()  # Query all lessons from the database
        serializer = LessonSerializer(lessons, many=True)  # Serialize the queryset
        return Response(serializer.data, status=200)  # Return serialized data
    def delete(self, request,lesson_id=None):
        try:
            Lesson.objects.filter(id=lesson_id).delete()  # Delete lessons associated with the course


            # Ensure the authenticated user is the instructor of the course
            # if course.instructor != request.user:
                # return Response({"detail": "You do not have permission to delete this lesson."}, status=status.HTTP_403_FORBIDDEN)

            return Response({"detail": "Lesson deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)
