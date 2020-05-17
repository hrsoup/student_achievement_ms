#教师子系统
from django.shortcuts import render,redirect
from django.http import HttpResponse

def teacher1(request):#个人信息
    return render(request,'teacher1.html')

def teacher2(request):#授课信息
    return render(request,'teacher2.html')

def teacher3(request):#学生成绩
    return render(request,'teacher3.html')

def indexTeacher(request):
    print("查询教师自己的信息")

def indexTCourse(request):
    print("查询教师教授的课程")

def indexTGrade(request):
    print("查询学生的成绩")

def indexTDist(request):
    print("查询学生成绩分布")