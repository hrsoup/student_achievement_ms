from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
def welcome(request):
    return render(request,'welcome.html')

def admin1(request): #个人信息
    
    return render(request,'admin1.html')


def admin2(request): #学生信息
    return render(request,'admin2.html')

def admin3(request): #教师信息
    return render(request,'admin3.html')

def admin4(request): #课程信息
    return render(request,'admin4.html')

def login(request):
    if(request.method=="POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        usertype=request.POST.get('my_select')
        #打印用于调试
        print("login POST username:",username)
        print("login POST password:",password)
        print("login POST usertype:",usertype)
        if(usertype=='student'):
            return redirect('/pro/student1')
        elif(usertype=='teacher'):
            return redirect('/pro/teacher1')
        else:
            return redirect('/pro/admin1')
    else:
        return render(request,'login.html')

def student1(request):#个人信息
    return render(request,'student1.html')

def indexStudent(request):
    print("indexStudent")

def indexSGPA(request):
    print("indexSGPA")

def indexSGPADIST(request):
    print("index")

def indexSCourse(request):
    print("indexSCourse")

def indexTeacher(request):
    print("查询教师自己的信息")

def indexTCourse(request):
    print("查询教师教授的课程")

def indexTGrade(request):
    print("查询学生的成绩")

def indexTDist(request):
    print("查询学生成绩分布")

def indexAdmin(request):
    print("查询管理员个人信息")

def indexAllStu(request):
    print("查询所有学生信息")

def indexAllTeacher(request):
    print("查询所有教师信息")

def indexAllCourse(request):
    print("查询所有课程信息")

def student2(request):#选课信息
    return render(request,'student2.html')

def student3(request):#选课成绩
    return render(request,'student3.html')

def teacher1(request):#个人信息
    return render(request,'teacher1.html')

def teacher2(request):#授课信息
    return render(request,'teacher2.html')

def teacher3(request):#学生成绩
    return render(request,'teacher3.html')

