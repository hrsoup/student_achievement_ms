#学生子系统
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection

def student1(request):#个人信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        return render(request,'student1.html')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def student2(request):#选课信息
    return render(request,'student2.html')

def student3(request):#选课成绩
    return render(request,'student3.html')

def indexStudent(request):
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select student_id,student_name,s.class_id,dept,major\
                        from student as s,class as c\
                        where s.student_id=%s and s.class_id=c.class_id;",[request.session['id']])   #根据具体学生id查询学生数据
        tmp = ('student_ID','student_name','class_ID','dept','major')  #返回的字段名
        result_list = []
        result = cursor.fetchone()
        result_list.append(dict(zip(tmp,result)))
        print(result_list)
        return redirect('/pro/student1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexSGPA(request):
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select course_name,grade\
                        from take as t,course as c\
                        where student_id=%s and t.course_id=c.course_id;"\
                        ,[request.session['id']])   #根据具体学生id查询课程成绩列表
        result_list=[]
        result = cursor.fetchone()
        while result:
            result_list.append({result[0]:result[1]})   #result[0]为课程名，result[1]为对应的成绩
            result = cursor.fetchone()
        print(result_list)
        return redirect('/pro/student1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexSGPADIST(request):
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select grade,count(grade)\
                        from take\
                        where student_id=%s\
                        group by grade;",[request.session['id']])   #根据具体学生id查询成绩分布
        result_list=[]
        result = cursor.fetchone()
        while result:
            result_list.append({result[0]:result[1]})   #result[0]为成绩，result[1]为成绩出现的次数
            result = cursor.fetchone()
        print(result_list)
        return redirect('/pro/student1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexSCourse(request):
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select t.course_id,course_name,grade,credits\
                        from take as t,course as c\
                        where student_id=%s and t.course_id=c.course_id;",[request.session['id']])   #根据具体学生id查询课程信息
        tmp = ('course_id','course_name','grade','credits')  #返回的字段名
        result_list = []
        result = cursor.fetchone()
        while result:
            result_list.append(dict(zip(tmp,result)))
            result = cursor.fetchone()
        print(result_list)
        return redirect('/pro/student1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')