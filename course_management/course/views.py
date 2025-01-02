from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Quiz
from .serializers import CourseSerializer, LessonSerializer

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