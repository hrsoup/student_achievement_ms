#管理员子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages

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
            print("课程ID:%s 课程名:%s 学分:%f" % (result_list[i]['course_id'], result_list[i]['course_name']
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
        student_id = request.POST.get('student_id')

        cursor.execute("select * from student where student_id = '%s' " % (student_id))
        student = cursor.fetchall()

        if operation == 'add': #录入
            password = request.POST.get('password')
            student_name = request.POST.get('student_name')
            class_id = request.POST.get('class_id')

            cursor.execute("select * from class where class_id = '%s' " % (class_id))
            Class = cursor.fetchall()

            error_count = 0
            if len(student) != 0:
                print("此学生ID已经存在")
                messages.error(request,"此学生ID已经存在")
                error_count += 1
            elif len(Class) == 0:
                print("该班级不存在")
                messages.error(request,"该班级不存在") 
                error_count += 1     
            elif error_count == 0:  
                cursor.execute('insert into student values \
                                ("%s", md5("%s"), "%s", "%s")' % (student_id, password, student_name, class_id))

        elif operation == 'update': #修改
            password = request.POST.get('password')
            student_name = request.POST.get('student_name')
            class_id = request.POST.get('class_id')

            cursor.execute("select * from class where class_id = '%s' " % (class_id))
            Class = cursor.fetchall()
            cursor.execute("select * from student where student_id = '%s' and class_id = '%s'" % (student_id, class_id))
            stu_class = cursor.fetchall()

            error_count = 0
            if len(student) == 0:
                print("此学生ID不存在")
                messages.error(request,"此学生ID不存在")
                error_count += 1
            elif len(Class) == 0:
                print("该班级不存在")
                messages.error(request,"该班级不存在") 
                error_count += 1     
            elif len(stu_class) == 0 and (error_count == 0):
                print("该学生不在此班级中")  
                messages.error(request,"该学生不在此班级中") 
                error_count += 1                    
            elif error_count == 0:  
                cursor.execute('update student set password = md5("%s"), student_name = "%s", class_id = "%s" where \
                            student_id = "%s"' % (password, student_name, class_id, student_id))

        elif operation == 'delete': #删除
            error_count = 0
            if len(student) == 0:
                print("此学生ID不存在")
                messages.error(request,"此学生ID不存在")
                error_count += 1
            elif error_count == 0:
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
        teacher_id = request.POST.get('teacher_id')
        cursor.execute("select * from teacher where teacher_id = '%s' " % (teacher_id))
        teacher = cursor.fetchall()

        if operation == 'add': #录入
            password = request.POST.get('password')
            teacher_name = request.POST.get('teacher_name')
            dept = request.POST.get('dept')

            error_count = 0
            if len(teacher) != 0:
                print("此教师ID已经存在")
                messages.error(request,"此教师ID已经存在")
                error_count += 1
            elif error_count == 0:  
                cursor.execute('insert into teacher values \
                            ("%s", md5("%s"), "%s", "%s")' % (teacher_id, password, teacher_name, dept))

        elif operation == 'update': #修改
            password = request.POST.get('password')
            teacher_name = request.POST.get('teacher_name')
            dept = request.POST.get('dept')

            error_count = 0
            if len(teacher) == 0:
                print("此教师ID不存在")
                messages.error(request,"此教师ID不存在")
                error_count += 1 
            elif error_count == 0:  
                cursor.execute('update teacher set password = md5("%s"), teacher_name = "%s", dept = "%s" \
                            where teacher_id = "%s"' % (password, teacher_name, dept, teacher_id))

        elif operation == 'delete': #删除
            error_count = 0
            if len(teacher) == 0:
                print("此教师ID不存在")
                messages.error(request,"此教师ID不存在")
                error_count += 1
            elif error_count == 0:  
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

def ifdigit(number):
    if type(eval(number)) != int and type(eval(number)) != float:
        return False
    else:
        return True

def changeAllCourse(request):#录入、删除、修改课程信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        course_id = request.POST.get('course_id')

        cursor.execute("select * from course where course_id = '%s' " % (course_id))
        course = cursor.fetchall()

        if operation == 'add': #录入
            course_name = request.POST.get('course_name')
            credit = request.POST.get('credits')
            error_count = 0
            if len(course) != 0:
                print("此课程ID已经存在")
                messages.error(request,"此课程ID已经存在")
                error_count += 1
            elif (ifdigit(credit) == False) or ((ifdigit(credit) == True) and (float(credit) < 0)):
                print("您输入的学分不是大于0的数字！")    
                messages.error(request,"您输入的学分不是大于0的数字！")
                error_count += 1  
            elif error_count == 0: 
                credit = float(credit)
                cursor.execute('insert into course values \
                            ("%s", "%s", "%f")' % (course_id, course_name, credit))

        elif operation == 'update': #修改
            course_name = request.POST.get('course_name')
            credit = request.POST.get('credits')
            cursor.execute("select * from course where course_id = '%s' and course_name = '%s' " % (course_id, course_name))
            class_course = cursor.fetchall()

            error_count = 0
            if len(course) == 0:
                print("此课程ID不存在")
                messages.error(request,"此课程ID不存在")
                error_count += 1
            elif len(class_course) == 0 and error_count == 0:
                print("此课程ID与课程名不对应")
                messages.error(request,"此课程ID与课程名不对应")
                error_count += 1    
            elif (ifdigit(credit) == False) or ((ifdigit(credit) == True) and (float(credit) < 0)):
                print(float(credit))
                print("您输入的学分不是大于0的数字！")    
                messages.error(request,"您输入的学分不是大于0的数字！")
                error_count += 1              
            elif error_count == 0: 
                credit = float(credit)
                cursor.execute('update course set course_name = "%s", credits = "%f" where \
                            course_id = "%s"' % (course_name, credit, course_id))

        elif operation == 'delete': #删除
            error_count = 0
            if len(course) == 0:
                print("此课程ID不存在")
                messages.error(request,"此课程ID不存在")
                error_count += 1
            elif error_count == 0: 
                cursor.execute('delete from course where course_id = "%s"' % (course_id))

        cursor.execute("select * from course;")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"course_id":r[0],'course_name':r[1],'credits':r[2]})
        for i in range(0, len(result_list)):
            print("课程ID:%s 课程名:%s 学分:%f" % (result_list[i]['course_id'], result_list[i]['course_name']
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
        class_id = request.POST.get('class_id')
        dept = request.POST.get('dept')
        major = request.POST.get('major')

        cursor.execute("select * from class where class_id = '%s' " % (class_id))
        Class = cursor.fetchall()

        if operation == 'add': #录入
            error_count = 0
            if len(Class) != 0:
                print("此班级ID已经存在")
                messages.error(request,"此班级ID已经存在")
                error_count += 1
            elif error_count == 0: 
                cursor.execute('insert into class values \
                            ("%s", "%s", "%s")' % (class_id, dept, major))

        elif operation == 'update': #修改
            error_count = 0
            if len(Class) == 0:
                print("此班级ID不存在")
                messages.error(request,"此班级ID不存在")
                error_count += 1
            elif error_count == 0: 
                cursor.execute('update class set dept = "%s", major = "%s" where \
                            class_id = "%s"' % (dept, major, class_id))

        elif operation == 'delete': #删除
            error_count = 0
            if len(Class) == 0:
                print("此班级ID不存在")
                messages.error(request,"此班级ID不存在")
                error_count += 1
            elif error_count == 0: 
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


def indexAlltake(request):#查询学生选课信息
    print("查询所有学生选课信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select take.student_id, student_name, take.course_id, course_name from \
                        take natural join student natural join course")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"student_id":r[0],'student_name':r[1],'course_id':r[2], 'course_name':r[3]})
        for i in range(0, len(result_list)):
            print("学生ID:%s 学生名字:%s 课程ID:%s 课程名字:%s" % (result_list[i]['student_id'], result_list[i]['student_name']
                                            , result_list[i]['course_id'], result_list[i]['course_name']))
        return render(request, 'admin6.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def changealltake(request):#录入、查询、修改学生选课信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')

        cursor.execute("select * from student where student_id = '%s' " % (student_id))
        student = cursor.fetchall()

        if operation == 'add': #录入
            cursor.execute("select * from course where course_id = '%s' " % (course_id))
            course = cursor.fetchall()

            cursor.execute("select * from take where \
                            student_id = '%s' and course_id = '%s'" % (student_id, course_id))
            stu_class = cursor.fetchall()

            error_count = 0

            if len(student) == 0:
                print("该学生ID不存在")
                messages.error(request,"该学生ID不存在")
                error_count += 1      
            elif len(course) == 0:
                print("该课程ID不存在")
                messages.error(request,"该课程ID不存在")
                error_count += 1             
            elif len(stu_class) != 0:
                print("此学生已经选中该课程")
                messages.error(request,"此学生已经选中该课程")
                error_count += 1
            elif error_count == 0: 
                grade = 0
                cursor.execute('insert into take values \
                            ("%s", "%s", "%f")' % (student_id, course_id, grade))


        elif operation == 'delete': #删除
            cursor.execute("select * from course where course_id = '%s' " % (course_id))
            course = cursor.fetchall()

            cursor.execute("select * from take where \
                            student_id = '%s' and course_id = '%s'" % (student_id, course_id))
            stu_class = cursor.fetchall()

            error_count = 0
            if len(student) == 0:
                print("该学生ID不存在")
                messages.error(request,"该学生ID不存在")
                error_count += 1      
            elif len(course) == 0:
                print("该课程ID不存在")
                messages.error(request,"该课程ID不存在")
                error_count += 1             
            elif len(stu_class) == 0:
                print("此学生并未选中该课程")
                messages.error(request,"此学生并未选中该课程")
                error_count += 1
            elif error_count == 0: 
                cursor.execute('delete from take where student_id = "%s" and course_id = "%s"' % (student_id, course_id))

        cursor.execute("select take.student_id, student_name, take.course_id, course_name from \
                        take natural join student natural join course")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"student_id":r[0],'student_name':r[1],'course_id':r[2], 'course_name':r[3]})
        for i in range(0, len(result_list)):
            print("学生ID:%s 学生名字:%s 课程ID:%s 课程名字:%s" % (result_list[i]['student_id'], result_list[i]['student_name']
                                            , result_list[i]['course_id'], result_list[i]['course_name']))
        return render(request, 'admin6.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')


def indexAllteach(request):#查询教师授课信息
    print("查询教师授课信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select teach.teacher_id, teacher_name, teach.course_id, course_name from \
                        teach natural join teacher natural join course")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"teacher_id":r[0],'teacher_name':r[1],'course_id':r[2], 'course_name':r[3]})
        for i in range(0, len(result_list)):
            print("教师ID:%s 教师名字:%s 课程ID:%s 课程名字:%s" % (result_list[i]['teacher_id'], result_list[i]['teacher_name']
                                            , result_list[i]['course_id'], result_list[i]['course_name']))
        return render(request, 'admin7.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')   

def changeallteach(request):#录入、查询、修改教师授课信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'admin':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        teacher_id = request.POST.get('teacher_id')
        course_id = request.POST.get('course_id')

        cursor.execute("select * from teacher where teacher_id = '%s' " % (teacher_id))
        teacher = cursor.fetchall()

        if operation == 'add': #录入
            cursor.execute("select * from course where course_id = '%s' " % (course_id))
            course = cursor.fetchall()

            cursor.execute("select * from teach where \
                            teacher_id = '%s' and course_id = '%s'" % (teacher_id, course_id))
            tea_course = cursor.fetchall()

            error_count = 0
            if len(teacher) == 0:
                print("该教师ID不存在")
                messages.error(request,"该教师ID不存在")
                error_count += 1      
            elif len(course) == 0:
                print("该课程ID不存在")
                messages.error(request,"该课程ID不存在")
                error_count += 1             
            elif len(tea_course) != 0:
                print("此教师已经教授该课程")
                messages.error(request,"此教师已经教授该课程")
                error_count += 1
            elif error_count == 0: 
                grade = 0
                cursor.execute('insert into teach values \
                            ("%s", "%s")' % (teacher_id, course_id))

        elif operation == 'delete': #删除
            cursor.execute("select * from course where course_id = '%s' " % (course_id))
            course = cursor.fetchall()

            cursor.execute("select * from teach where \
                            teacher_id = '%s' and course_id = '%s'" % (teacher_id, course_id))
            tea_course = cursor.fetchall()
            
            error_count = 0
            if len(teacher) == 0:
                print("该教师ID不存在")
                messages.error(request,"该教师ID不存在")
                error_count += 1      
            elif len(course) == 0:
                print("该课程ID不存在")
                messages.error(request,"该课程ID不存在")
                error_count += 1             
            elif len(tea_course) == 0:
                print("此教师并未教授该课程")
                messages.error(request,"此教师并未教授该课程")
                error_count += 1
            elif error_count == 0: 
                cursor.execute('delete from teach where teacher_id = "%s" and course_id = "%s"' % (teacher_id, course_id))

        cursor.execute("select teach.teacher_id, teacher_name, teach.course_id, course_name from \
                        teach natural join teacher natural join course")
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"teacher_id":r[0],'teacher_name':r[1],'course_id':r[2], 'course_name':r[3]})
        for i in range(0, len(result_list)):
            print("教师ID:%s 教师名字:%s 课程ID:%s 课程名字:%s" % (result_list[i]['teacher_id'], result_list[i]['teacher_name']
                                            , result_list[i]['course_id'], result_list[i]['course_name']))
        return render(request, 'admin7.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')