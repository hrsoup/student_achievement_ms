#教师子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from dbms.view.pageholder import pageBuilder

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
        return render(request, 'teacher1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexTCourse(request):#查询所授课程信息
    print("查询教师教授的课程")
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select course.course_id,course_name,credits \
                        from course natural join teach \
                        where teacher_id='%s' \
                        order by course.course_id;" % (teacher_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"course_id":r[0],'course_name':r[1],'credits':r[2]})
        return render(request, 'teacher2.html', pageBuilder(result_list,page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexTGrade(request):#查询所授课程学生成绩信息
    print("查询学生的成绩")
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select take.student_id,student_name,take.course_id,course_name,credits,grade \
                        from student natural join course natural join take natural join teach \
                        where teacher_id ='%s' \
                        order by take.student_id, take.course_id;" % (teacher_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"student_id":r[0],'student_name':r[1],'course_id':r[2],\
                                'course_name':r[3],'credits':r[4],'grade':r[5]})
        return render(request, 'teacher3.html',pageBuilder(result_list,page))
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def ifdigit(num):
    if num.replace(".",'').isdigit():
        if num.count(".")==0:
            return True
        elif num.count(".")==1:
            return True
    else: 
        return False


def changeTGrade(request):#录入、删除、修改所授课程学生成绩信息
    page=request.GET.get('page',1)
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher':
        teacher_id = request.session['id']
        connection.connect()
        cursor = connection.cursor()
        operation = request.POST.get('my_select')
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')

        cursor.execute("select * from student where student_id = '%s' " % (student_id))
        student = cursor.fetchall()
        cursor.execute("select * from course where course_id = '%s' " % (course_id))
        course = cursor.fetchall()

        if operation == 'update': #修改
            grade = request.POST.get('grade')
            cursor.execute("select * from take \
                            where course_id = '%s' and student_id = '%s'" % (course_id, student_id))
            grades = cursor.fetchall()
            error_count = 0 
            if len(student) == 0:
                print("该学生不存在")
                messages.error(request,"该学生不存在")
                error_count += 1
            elif len(course) == 0:
                print("该课程不存在")
                messages.error(request,"该课程不存在") 
                error_count += 1
            elif len(grades) ==0 and (error_count == 0):
                print("该学生没有上此门课程")  
                messages.error(request,"该学生没有上此门课程") 
                error_count += 1         
            elif (ifdigit(grade) == False) or ((ifdigit(grade) == True) and ((float(grade) < 0) or (float(grade) > 100))):
                print("请输入0到100之间的数字")    
                messages.error(request,"请输入0到100之间的数字")
                error_count += 1  
            elif error_count == 0:
                grade = float(grade)
                cursor.execute('update take set \
                                grade = "%f" where (student_id = "%s") \
                                and (course_id = "%s")' % (grade, student_id, course_id))

        cursor.execute("select take.student_id,student_name,take.course_id,course_name,credits,grade \
                        from student natural join course natural join take natural join teach \
                        where teacher_id ='%s' \
                        order by take.student_id, take.course_id;" % (teacher_id))
        result = cursor.fetchall()
        connection.close()
        result_list = []
        for r in result:
            result_list.append({"student_id":r[0],'student_name':r[1],'course_id':r[2],\
                                'course_name':r[3],'credits':r[4],'grade':r[5]})
        return render(request, 'teacher3.html',pageBuilder(result_list,page))

    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')