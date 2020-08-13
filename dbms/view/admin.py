#管理员子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse

def admin(request): #个人信息
    return render(request,'admin.html')

def indexAdmin(request):#查询管理员个人信息
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
        for i in range(0,len(result_list)):
            print("管理员ID:%s 姓名:%s" % (result_list[i]['admin_id'], result_list[i]['admin_name']))
        return render(request, 'admin1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexAllStu(request):#查询所有学生信息
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
        for i in range(0, len(result_list)):
            print("学生ID:%s 登录密码:%s 姓名:%s 所在学院:%s 所在专业:%s 所在班级:%s" % (result_list[i]['student_id'], result_list[i]['password']
           ,result_list[i]['student_name'], result_list[i]['dept'],result_list[i]['major'],result_list[i]['class_id']))
        return render(request, 'admin2.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexAllTeacher(request):#查询所有教师信息
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
        for i in range(0, len(result_list)):
            print("教师ID:%s 登录密码:%s 姓名:%s 所在学院:%s" % (result_list[i]['teacher_id'], result_list[i]['password']
                                            , result_list[i]['teacher_name'],result_list[i]['dept']))
        return render(request, 'admin3.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexAllCourse(request):#查询所有课程信息
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
        for i in range(0, len(result_list)):
            print("课程ID:%s 课程名:%s 学分:%d" % (result_list[i]['course_id'], result_list[i]['course_name']
                                            , result_list[i]['credits']))
        return render(request, 'admin4.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

#def changeAllStu(request):录入、删除、修改学生信息
#def changeAllTeacher(request):录入、删除、修改教师信息
#def changeAllCourse(request):录入、删除、修改课程信息