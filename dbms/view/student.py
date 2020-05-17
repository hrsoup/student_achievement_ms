#学生子系统
from django.shortcuts import render,redirect
from django.http import HttpResponse

def student1(request):#个人信息
    return render(request,'student1.html')

def student2(request):#选课信息
    return render(request,'student2.html')

def student3(request):#选课成绩
    return render(request,'student3.html')

def indexStudent(request):
    print("indexStudent")

def indexSGPA(request):
    print("indexSGPA")

def indexSGPADIST(request):
    print("index")

def indexSCourse(request):
    print("indexSCourse")