#学生子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse

def student(request):
    return render(request,'student.html')

def indexStudent(request):
    print("查询学生自己的信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select student_id,student_name,s.class_id,dept,major\
                        from student as s,class as c\
                        where s.student_id=%s and s.class_id=c.class_id;",[request.session['id']])#根据具体学生id查询学生数据
        tmp = ('student_ID','student_name','class_ID','dept','major')#返回的字段名
        result_list = []
        result = cursor.fetchone()
        result_list.append(dict(zip(tmp,result)))
        for i in range(0, len(result_list)):
            print("学生id:%s 姓名:%s 所在学院:%s 所在专业:%s 所在班级:%s"%(result_list[i]['student_ID'],result_list[i]['student_name']
            ,result_list[i]['dept'],result_list[i]['major'],result_list[i]['class_ID']))
        return render(request, 'student1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexSCourse(request):
    print("查询学生选课信息")
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
        for i in range(0, len(result_list)):
            print("课程ID:%s 课程名:%s 学分:%d" %(result_list[i]['course_id'],result_list[i]['course_name']
            ,result_list[i]['credits']))
        #html网页做表格结构动态变化并且将cmd输出的内容更新到界面上进行对应显示
        return render(request, 'student2.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

def indexSGPA(request):
    print("查询学生自己的成绩")
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
        for i in range(0, len(result_list)):
            print("课程ID:%s 课程名:%s 成绩:%d" % (result_list[i]['course_id'], result_list[i]['course_name']
            ,result_list[i]['grade']))
        return render(request, 'student3.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')