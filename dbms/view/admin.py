#管理员子系统
from django.shortcuts import render,redirect
from django.http import HttpResponse

def admin1(request): #个人信息
    return render(request,'admin1.html')

def admin2(request): #学生信息
    return render(request,'admin2.html')
    
def admin3(request): #教师信息
    return render(request,'admin3.html')

def admin4(request): #课程信息
    return render(request,'admin4.html')

def indexAdmin(request):
    print("查询管理员个人信息")

def indexAllStu(request):
    print("查询所有学生信息")

def indexAllTeacher(request):
    print("查询所有教师信息")

def indexAllCourse(request):
    print("查询所有课程信息")