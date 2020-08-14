#教师子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse

def teacher(request):#个人信息
    return render(request,'teacher.html')

def indexTeacher(request):#查询教师个人信息
    print("查询教师自己的信息")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher': 
        teacher_id = request.session['id']
        connection.connect()  
        cursor = connection.cursor()
        cursor.execute("select * from teacher where teacher_id='%s'" % (teacher_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"teacher_id":r[0],'teacher_name':r[2],'dept':r[3]})
        for i in range(0, len(result_list)):
            print("教师id:%s 姓名:%s 所在学院:%s " % (result_list[i]['teacher_id'], result_list[i]['teacher_name']
                                                           , result_list[i]['dept']))
        return render(request, 'teacher1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexTCourse(request):#查询所授课程信息
    print("查询教师教授的课程")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select course.course_id,course_name,credits \
                        from course natural join teach \
                        where teacher_id='%s'" % (teacher_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"course_id":r[0],'course_name':r[1],'credits':r[2]})
        for i in range(0, len(result_list)):
            print("课程ID:%s 课程名:%s 学分:%d" % (result_list[i]['course_id'], result_list[i]['course_name']
                                            , result_list[i]['credits']))
        return render(request, 'teacher2.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexTGrade(request):#查询所授课程学生成绩信息
    print("查询学生的成绩")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select take.student_id,student_name,take.course_id,course_name,credits,grade \
                        from student natural join course natural join take natural join teach \
                        where teacher_id ='%s'" % (teacher_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"student_id":r[0],'student_name':r[1],'course_id':r[2],\
                                'course_name':r[3],'credits':r[4],'grade':r[5]})
        for i in range(0,len(result_list)):
            print("学生ID:%s 学生姓名:%s 课程ID:%s 课程名:%s 学分:%d 成绩：%d" % (result_list[i]['student_id'], result_list[i]['student_name']
            , result_list[i]['course_id'], result_list[i]['course_name'], result_list[i]['credits'],result_list[i]['grade']))
        return render(request, 'teacher3.html',{"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def changeTGrade(request):#录入、删除、修改所授课程学生成绩信息
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')

        if operation == 'add': #录入
            student_id = request.POST.get('student_id')
            course_id = request.POST.get('course_id')
            grade = int(request.POST.get('grade'))
            cursor.execute('insert into take values \
                            ("%s", "%s", %d)' % (student_id, course_id, grade))

        elif operation == 'update': #修改
            student_id = request.POST.get('student_id')
            course_id = request.POST.get('course_id')
            grade = int(request.POST.get('grade'))
            cursor.execute('update take set \
                            grade = %d where (student_id = "%s") and (course_id = "%s")' % (grade, student_id, course_id))

        elif operation == 'delete': #删除
            student_id = request.POST.get('student_id')
            course_id = request.POST.get('course_id')
            cursor.execute('delete from take where student_id = "%s" and course_id = "%s"' % (student_id, course_id))


        cursor.execute("select take.student_id,student_name,take.course_id,course_name,credits,grade \
                        from student natural join course natural join take natural join teach \
                        where teacher_id ='%s'" % (teacher_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"student_id":r[0],'student_name':r[1],'course_id':r[2],\
                                'course_name':r[3],'credits':r[4],'grade':r[5]})
        for i in range(0,len(result_list)):
            print("学生ID:%s 学生姓名:%s 课程ID:%s 课程名:%s 学分:%d 成绩：%d" % (result_list[i]['student_id'], result_list[i]['student_name']
            , result_list[i]['course_id'], result_list[i]['course_name'], result_list[i]['credits'],result_list[i]['grade']))
        return render(request, 'teacher3.html',{"data": result_list})

    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')