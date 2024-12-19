 # **Project Overview**

This project is a modular backend system designed for an online learning platform, serving two primary user roles: **Students** and **Instructors**. The system is divided into three microservices—**Authentication Service**, **Course Management Service**, and **Notification Service**—to ensure scalability, maintainability, and clear responsibility boundaries.

# Microservices Communication and Configuration Setup  
**Felix Edesa**  
**December 2024**

## 1. Specification of Micro-services

The table below outlines the specification of the Authentication Service, Course Management Service, and Notification Service in the e-learning platform.

| **No** | **Micro-service**            | **Responsibilities**                                                                 | **Key Features**                                                                                      | **Database Entities**                                                    | **APIs**                                                                                   |
|--------|------------------------------|--------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| 1      | **Authentication Service**    | - Handles login, signup, and profile management.<br>- Manages role-based access control.<br>- Provides secure token-based authentication for other services. | - User registration and login for both students and instructors.<br>- Role-based access specific to students and instructors.<br>- Secure token-based authentication. | Users (students, instructors)                                              | POST /auth/signup: Register new user.<br>POST /auth/login: User login.<br>GET /auth/profile: Retrieve user profile.<br>GET /auth/validate-token: Token validation. |
| 2      | **Course Management Service** | - Manages course and quiz creation, including uploading materials.<br>- Handles course enrollment for students.<br>- Delivers learning materials and quizzes to students. | - Create and upload courses with lessons and quizzes.<br>- Manage student enrollment in courses.<br>- View lessons (text, videos, or files) and mark them as complete.<br>- Take quizzes and receive feedback.<br>- Track completed lessons and progress. | Courses, Lessons, Quizzes, Enrollments, StudentProgress                       | POST /courses: Create new course.<br>POST /courses/{courseId}/enroll: Enroll in a course.<br>GET /courses/{courseId}: Get course details.<br>GET /courses/{courseId}/lessons: Retrieve lessons for a course.<br>POST /quizzes/{lessonId}: Create a quiz for a lesson.<br>POST /quizzes/{quizId}/submit: Submit a quiz. |
| 3      | **Notification Service**      | - Create, schedule, and deliver notifications to users.                              | - Send OTP notification via email.<br>- Send lesson added notification via email. | Notifications                                                              | POST /notifications/otp: Send OTP notification.<br>POST /notifications/lesson-added: Send lesson added notification.<br>GET /notifications/status: Get notification status. |                                               |

## Archetecture

![E-learning Archetecture](e-learning.png)

