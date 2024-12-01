# **Project Overview**

This project is a modular backend system designed for an online learning platform, serving two primary user roles: **Students** and **Instructors**. The system is divided into three microservices—**Authentication Service**, **Course Management Service**, and **Learning Service**—to ensure scalability, maintainability, and clear responsibility boundaries.

---

## **Features**

### **For Students**
- **User Registration and Login**  
  - Basic authentication using email and password.  
  - Role-based access specific to students.

- **Course Enrollment**  
  - View available courses.  
  - Enroll in a course.

- **Access Learning Materials**  
  - View lessons, including text, PDFs, and videos.  
  - Mark lessons as complete.

- **Quizzes and Assessments**  
  - Take quizzes to test knowledge (e.g., multiple choice, true/false).  
  - Receive instant feedback on quiz completion.

- **Progress Tracking**  
  - View completed lessons and quiz scores.

---

### **For Instructors**
- **User Registration and Login**  
  - Basic authentication using email and password.  
  - Role-based access specific to instructors.

- **Course Creation**  
  - Create and manage courses with details like title, description, and lessons.  
  - Upload lesson materials, including text, video, or files.

- **Quiz Management**  
  - Add and manage quizzes for lessons.

---

## **Microservices**

### **1. Authentication Service**
- **Responsibilities**:  
  - Handles login, signup, and profile management.  
  - Manages role-based access control.  
  - Provides secure token-based authentication for other services.

- **Key Features**:  
  - User registration and login for both students and instructors.  
  - Exposes APIs to validate tokens and retrieve user profiles.

---

### **2. Course Management Service**
- **Responsibilities**:  
  - Manages course and quiz creation, including uploading materials.  
  - Handles course enrollment for students.

- **Key Features**:  
  - Create and upload courses with lessons and quizzes.  
  - Manage enrollment of students in courses.  
  - Provide APIs for lessons and quiz metadata for consumption by other services.

---

### **3. Learning Service**
- **Responsibilities**:  
  - Focuses on delivering learning materials and quizzes to students.  
  - Tracks student progress and quiz results.

- **Key Features**:  
  - View lessons (text, videos, or files) and mark them as complete.  
  - Take quizzes and receive feedback.  
  - Track completed lessons and progress.
 
## Archetecture

![E-learning Archetecture](Image_URL_or_Path)

