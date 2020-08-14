#学生子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import JsonResponse
from dbms.view.pageholder import pageBuilder


def student(request):
    return render(request,'student.html')

def indexStudent(request):#查询学生个人信息
    print("查询学生自己的信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select student_id,student_name,s.class_id,dept,major\
                        from student as s,class as c\
                        where s.student_id=%s and s.class_id=c.class_id;",[request.session['id']])#根据具体学生id查询学生数据
        tmp = ('student_id','student_name','class_id','dept','major')#返回的字段名
        result_list = []
        result = cursor.fetchone()
        result_list.append(dict(zip(tmp,result)))
        return render(request,'student1.html',{"data":result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexSCourse(request):#查询所选课程信息
    print("查询学生选课信息")
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select t.course_id,course_name,credits\
                        from take as t,course as c\
                        where student_id=%s and t.course_id=c.course_id;",[request.session['id']])#根据具体学生id查询课程信息
        tmp = ('course_id','course_name','credits')#返回的字段名
        result_list = []
        result = cursor.fetchone()
        while result:
            result_list.append(dict(zip(tmp,result)))
            result = cursor.fetchone()
        #html网页做表格结构动态变化并且将cmd输出的内容更新到界面上进行对应显示
        return render(request,'student2.html',pageBuilder(result_list,page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexSGPA(request):#查询选修成绩信息
    print("查询学生自己的成绩")
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select t.course_id,course_name,grade\
                        from take as t,course as c\
                        where student_id=%s and t.course_id=c.course_id;"\
                        ,[request.session['id']])#根据具体学生id查询课程成绩列表
        result_list=[]
        result = cursor.fetchone()
        tmp=('course_id','course_name','grade')
        while result:
            result_list.append(dict(zip(tmp,result)))
            result = cursor.fetchone()
        return render(request,'student3.html',pageBuilder(result_list,page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')