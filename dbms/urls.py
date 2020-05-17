from django.urls import path
from .view import add, admin, enroll, stat, student, teacher
urlpatterns = [
    path('welcome/',enroll.welcome),
    path('admin1/',admin.admin1), #个人信息
    path('admin2/',admin.admin2),
    path('admin3/',admin.admin3),
    path('admin4/',admin.admin4),
    path('login/',enroll.login),
    path('student1',student.student1),
    path('student2',student.student2),
    path('student3',student.student3),
    path('teacher1',teacher.teacher1),
    path('teacher2',teacher.teacher2),
    path('teacher3',teacher.teacher3),
    path('indexStudent',student.indexStudent),
    path('indexSCourse',student.indexSCourse),
    path('indexSGPA',student.indexSGPA),
    path('indexSGPADIST',student.indexSGPADIST),
    path('indexTeacher',teacher.indexTeacher),
    path('indexTCourse',teacher.indexTCourse),
    path('indexTGrade',teacher.indexTGrade),
    path('indexTDist',teacher.indexTDist),
    path('indexAdmin',admin.indexAdmin),
    path('indexAllStu',admin.indexAllStu),
    path('indexAllTeacher',admin.indexAllTeacher),
    path('indexAllCourse',admin.indexAllCourse),
]