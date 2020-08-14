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

def changeAllStu(request):#录入、删除、修改学生信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        admin_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')

        if operation == 'add': #录入
            student_id = request.POST.get('student_id')
            password = request.POST.get('password')
            student_name = request.POST.get('student_name')
            class_id = request.POST.get('class_id')
            cursor.execute('insert into student values \
                            ("%s", md5("%s"), "%s", "%s")' % (student_id, password, student_name, class_id))

        elif operation == 'update': #修改
            student_id = request.POST.get('student_id')
            password = (request.POST.get('password'))
            student_name = request.POST.get('student_name')
            class_id = request.POST.get('class_id')
            cursor.execute('update student set password = md5("%s"), student_name = "%s", class_id = "%s" where \
                            student_id = "%s"' % (password, student_name, class_id, student_id))

        elif operation == 'delete': #删除
            student_id = request.POST.get('student_id')
            cursor.execute('delete from student where student_id = "%s"' % (student_id))

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


def changeAllTeacher(request):#录入、删除、修改教师信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')

        if operation == 'add': #录入
            teacher_id = request.POST.get('teacher_id')
            password = request.POST.get('password')
            teacher_name = request.POST.get('teacher_name')
            dept = request.POST.get('dept')
            cursor.execute('insert into teacher values \
                            ("%s", md5("%s"), "%s", "%s")' % (teacher_id, password, teacher_name, dept))

        elif operation == 'update': #修改
            teacher_id = request.POST.get('teacher_id')
            password = request.POST.get('password')
            teacher_name = request.POST.get('teacher_name')
            dept = request.POST.get('dept')
            cursor.execute('update teacher set password = md5("%s"), teacher_name = "%s", dept = "%s" \
                            where teacher_id = "%s"' % (password, teacher_name, dept, teacher_id))

        elif operation == 'delete': #删除
            teacher_id = request.POST.get('teacher_id')
            cursor.execute('delete from teacher where teacher_id = "%s"' % (teacher_id))

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


def changeAllCourse(request):#录入、删除、修改课程信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')

        if operation == 'add': #录入
            course_id = request.POST.get('course_id')
            course_name = request.POST.get('course_name')
            credit = int(request.POST.get('credits'))
            cursor.execute('insert into course values \
                            ("%s", "%s", %d)' % (course_id, course_name, credit))

        elif operation == 'update': #修改
            course_id = request.POST.get('course_id')
            course_name = request.POST.get('course_name')
            credit = int(request.POST.get('credits'))
            cursor.execute('update course set course_name = "%s", credits = %d where \
                            course_id = "%s"' % (course_name, credit, course_id))

        elif operation == 'delete': #删除
            course_id = request.POST.get('course_id')
            cursor.execute('delete from course where course_id = "%s"' % (course_id))

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

def indexAllClass(request):#查询班级信息
    print("查询所有班级信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select * from class")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"class_id":r[0],'dept':r[1],'major':r[2]})
        for i in range(0, len(result_list)):
            print("班级ID:%s 院系:%s 专业:%s" % (result_list[i]['class_id'], result_list[i]['dept']
                                            , result_list[i]['major']))
        return render(request, 'admin5.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def changeallClass(request):#录入、删除、修改班级信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')

        if operation == 'add': #录入
            class_id = request.POST.get('class_id')
            dept = request.POST.get('dept')
            major = request.POST.get('major')
            cursor.execute('insert into class values \
                            ("%s", "%s", "%s")' % (class_id, dept, major))

        elif operation == 'update': #修改
            class_id = request.POST.get('class_id')
            dept = request.POST.get('dept')
            major = request.POST.get('major')
            cursor.execute('update class set dept = "%s", major = "%s" where \
                            class_id = "%s"' % (dept, major, class_id))

        elif operation == 'delete': #删除
            class_id = request.POST.get('class_id')
            cursor.execute('delete from class where class_id = "%s"' % (class_id))

        cursor.execute("select * from class")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"class_id":r[0],'dept':r[1],'major':r[2]})
        for i in range(0, len(result_list)):
            print("班级ID:%s 院系:%s 专业:%s" % (result_list[i]['class_id'], result_list[i]['dept']
                                            , result_list[i]['major']))
        return render(request, 'admin5.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')