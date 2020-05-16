from django.urls import path
from . import views
urlpatterns = [
    path('welcome/',views.welcome),
    path('admin1/',views.admin1), #个人信息
    path('admin2/',views.admin2),
    path('admin3/',views.admin3),
    path('admin4/',views.admin4),
    path('login/',views.login),
    path('student1',views.student1),
    path('student2',views.student2),
    path('student3',views.student3),
    path('teacher1',views.teacher1),
    path('teacher2',views.teacher2),
    path('teacher3',views.teacher3),
    path('indexStudent',views.indexStudent),
    path('indexSCourse',views.indexSCourse),
    path('indexSGPA',views.indexSGPA),
    path('indexSGPADIST',views.indexSGPADIST),
    path('indexTeacher',views.indexTeacher),
    path('indexTCourse',views.indexTCourse),
    path('indexTGrade',views.indexTGrade),
    path('indexTDist',views.indexTDist),
    path('indexAdmin',views.indexAdmin),
    path('indexAllStu',views.indexAllStu),
    path('indexAllTeacher',views.indexAllTeacher),
    path('indexAllCourse',views.indexAllCourse),
]