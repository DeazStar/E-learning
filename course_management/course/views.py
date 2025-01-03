from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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



# Delete Course
class DeleteCourseView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
      courses = Course.objects.all()  # Query all courses from the database
      serializer = CourseSerializer(courses, many=True)  # Serialize the queryset
      return Response(serializer.data, status=200)  # Return serialized data

    def delete(self, request):
        
        try:

            course = Course.objects.all()
            # Ensure the authenticated user is the instructor
            # if course.instructor != request.user:
                # return Response({"detail": "You do not have permission to delete this course."}, status=status.HTTP_403_FORBIDDEN)
            course.delete()
            return Response({"detail": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

# Delete Lesson
class DeleteLessonView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        lessons = Lesson.objects.all()  # Query all lessons from the database
        serializer = LessonSerializer(lessons, many=True)  # Serialize the queryset
        return Response(serializer.data, status=200)  # Return serialized data
    def delete(self, request):
        try:
            lesson = Lesson.objects.all()  # Query all lessons from the database


            # Ensure the authenticated user is the instructor of the course
            # if course.instructor != request.user:
                # return Response({"detail": "You do not have permission to delete this lesson."}, status=status.HTTP_403_FORBIDDEN)

            lesson.delete()
            return Response({"detail": "Lesson deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)



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