#管理员子系统
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection

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
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin': 
        admin_id = request.session['id']
        connection.connect()  
        cursor = connection.cursor()
        cursor.execute("select * from admin where admin_id='%s'" % (admin_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"admin_id":r[0],'admin_name':r[2]})
        print(result_list)
        return redirect('/pro/admin1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexAllStu(request):
    print("查询所有学生信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin': 
        admin_id = request.session['id']
        connection.connect()  
        cursor = connection.cursor()
        cursor.execute("select student.student_id,password,student_name,dept,major,class.class_id \
                        from student natural join class;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"student_id":r[0],'password':r[1],'student_name':r[2],\
                                'dept':r[3],'major':r[4],'class_id':r[5]})
        print(result_list)
        return redirect('/pro/admin1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexAllTeacher(request):
    print("查询所有教师信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin': 
        teacher_id = request.session['id']
        connection.connect()  
        cursor = connection.cursor()
        cursor.execute("select * from teacher;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"teacher_id":r[0],"password":r[1],'teacher_name':r[2],'dept':r[3]})
        print(result_list)
        return redirect('/pro/admin1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexAllCourse(request):
    print("查询所有课程信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin': 
        teacher_id = request.session['id']
        connection.connect()  
        cursor = connection.cursor()
        cursor.execute("select * from course;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"course_id":r[0],'course_name':r[1],'credits':r[2]})
        print(result_list)
        return redirect('/pro/admin1')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')
