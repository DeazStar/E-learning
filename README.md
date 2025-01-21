# **Project Overview**

This project is a modular backend system designed for an online learning platform, serving two primary user roles: **Students** and **Instructors**. The system is divided into three microservices—**Authentication Service**, **Course Management Service**, and **Notification Service**—to ensure scalability, maintainability, and clear responsibility boundaries.

# Microservices Communication and Configuration Setup  

## 1. Specification of Micro-services

The table below outlines the specification of the Authentication Service, Course Management Service, and Notification Service in the e-learning platform.

| **No** | **Micro-service**            | **Responsibilities**                                                                 | **Key Features**                                                                                      | **Database Entities**                                                    | **APIs**                                                                                   |
|--------|------------------------------|--------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| 1      | **Authentication Service**    | - Handles login, signup, and profile management.<br>- Manages role-based access control.<br>- Provides secure token-based authentication for other services. | - User registration and login for both students and instructors.<br>- Role-based access specific to students and instructors.<br>- Secure token-based authentication. | Users (students, instructors)                                              | POST /api/users/register: Register new user.<br>POST /api/users/login: User login.<br>GET /api/users/get_me: Retrieve user profile.<br>GET /api/users/verify-token: Token validation. |
| 2      | **Course Management Service** | - Manages course and quiz creation, including uploading materials.<br>- Handles course enrollment for students.<br>- Delivers learning materials and quizzes to students. | - Create and upload courses with lessons and quizzes.<br>- Manage student enrollment in courses.<br>- View lessons (text, videos, or files) and mark them as complete.<br>- Take quizzes and receive feedback.<br>- Track completed lessons and progress. | Courses, Lessons, Quizzes, Enrollments, StudentProgress                       | POST /api/courses: Create new course.<br>POST /api/courses/{courseId}/enroll: Enroll in a course.<br>GET /api/courses/{courseId}: Get course details.<br>GET /api/courses/{courseId}/lessons: Retrieve lessons for a course.<br>POST /api/course/quizzes/{lessonId}: Create a quiz for a lesson.<br>POST /api/course/quizzes/{quizId}/submit: Submit a quiz. |
| 3      | **Notification Service**      | - Create, schedule, and deliver notifications to users.                              | - Send OTP notification via email.<br>- Send welcome notification via email when user register. | Notifications                                                              | |                                               |

## Archetecture

![E-learning Archetecture](e-learning.png)

