#统计子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse
import matplotlib
matplotlib.use('Agg')   #使用matplotlib的非交互式后端Agg，以解决Tcl_AsyncDelete问题
import matplotlib.pyplot as plt
import os
import re

plt.rcParams['font.sans-serif']=['SimHei']  #能显示中文标签
#某个学生所有课程成绩分布的统计函数，成绩段：0-59、60-69、70-79、80-89、90-100
def indexSGPADIST(request):
    print("查询成绩分布")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        studentId = request.session['id']
        #首先先将之前该学生对应的统计图片删掉
        picreg = "^[^_]*_" + studentId + "\.jpg$"
        for pic in os.listdir("static/student_stat_img/"):
            if re.match(picreg, pic) != None:
                os.remove("static/student_stat_img/" + pic)
        connection.connect()
        cursor = connection.cursor()
        #获取学生名字
        cursor.execute("select student_name\
                        from student\
                        where student_id=%s;",[request.session['id']])
        result = cursor.fetchone()
        student_name = result[0]
        #查询学生成绩分布
        cursor.execute("select grade,count(grade) as counts\
                        from take\
                        where student_id=%s\
                        group by grade;",[studentId])   #根据具体学生id查询成绩分布
        result_list=[]
        result = cursor.fetchone()
        tmp=('grade','counts')
        while result:
            result_list.append(dict(zip(tmp, result)))
            result = cursor.fetchone()
        for i in range(0, len(result_list)):
            print("取得成绩:%d 对应次数:%d" % (result_list[i]['grade'], result_list[i]['counts']))
        num_list = [0, 0, 0, 0, 0]
        label_list = ["0-59分", "60-69分", "70-79分", "80-89分", "90-100分"]
        color_list = ["royalblue","darkcyan","yellowgreen","yellow","orangered"]
        for i in range(len(result_list)):
            grade = result_list[i]['grade']
            if grade >= 0 and grade <= 59:
                num_list[0] += result_list[i]['counts']
            elif grade >= 60 and grade <= 69:
                num_list[1] += result_list[i]['counts']
            elif grade >= 70 and grade <= 79:
                num_list[2] += result_list[i]['counts']
            elif grade >= 80 and grade <= 89:
                num_list[3] += result_list[i]['counts']
            else:
                num_list[4] += result_list[i]['counts']
        #柱状图
        plt.title('直方图')
        plt.xlabel('分数段')
        plt.ylabel('计数')
        if max(num_list) <= 4:
            plt.yticks(list(range(max(num_list) + 1)))
        plt.bar(range(len(num_list)), num_list, color=color_list, tick_label=label_list)
        plt.savefig("static/student_stat_img/bar_" + studentId + ".jpg")  #图片拿学生id作为标识
        plt.close()
        #饼图
        #获得个数非0的成绩段（以及相应的label_list和color_list）
        pie_num_list, pie_label_list, pie_color_list = [], [], []
        for i in range(len(num_list)):
            if num_list[i] > 0:
                pie_num_list.append(num_list[i])
                pie_label_list.append(label_list[i])
                pie_color_list.append(color_list[i])
        plt.title('饼状图')
        plt.pie(pie_num_list, labels=pie_label_list, colors=pie_color_list, autopct='%1.2f%%', textprops={'fontsize':12,'color':'black'})
        plt.axis('equal')
        plt.savefig("static/student_stat_img/pie_" + studentId + ".jpg")#图片拿学生id作为标识
        plt.close()
        #将具体数据和图片所在路径包装成一个字典返回给前端
        data = {}
        data["data"] = result_list
        data["bar"] = "student_stat_img/bar_" + studentId + ".jpg"
        data["pie"] = "student_stat_img/pie_" + studentId + ".jpg"
        data["student_name"] = student_name
        return render(request, 'student4.html', data)
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

#教师成绩分布的统计函数
def indexTDistSelect(request):#获取下拉框
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
            print("课程ID:%s 课程名:%s" % (result_list[i]['course_id'], result_list[i]['course_name']))
        return render(request, 'teacher4-1.html', {"data": result_list})
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')

def indexTDistShow(request):#获取下拉框和成绩统计分布的对应图片
    print("查询教师教授的课程以及该课程所有学生的成绩分布")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'teacher':
        teacher_id = request.session['id']
        course_id = request.POST.get('my_select')
        #首先先将之前该教师对应课程的统计图片删掉
        picreg = "^[^_]*_" + teacher_id + '_' + course_id + "\.jpg$"
        for pic in os.listdir("static/teacher_stat_img/"):
            if re.match(picreg, pic) != None:
                os.remove("static/teacher_stat_img/" + pic)
        #先查询教师教授的所有课程信息，以及该课程id对应的课程名
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select course.course_id,course_name,credits \
                        from course natural join teach \
                        where teacher_id='%s'" % (teacher_id))
        result = cursor.fetchall()
        result_list = []
        course_name = ""
        for r in result:
            result_list.append({"course_id":r[0],'course_name':r[1],'credits':r[2]})
            if r[0] == course_id:
                course_name = r[1]
        #查询该课程的学生成绩分布
        cursor.execute("select grade,count(grade) as counts\
                        from take\
                        where course_id=%s\
                        group by grade;",[course_id])   #根据具体课程id查询成绩分布
        grade_list=[]
        result = cursor.fetchone()
        tmp=('grade','counts')
        while result:
            grade_list.append(dict(zip(tmp, result)))
            result = cursor.fetchone()
        connection.close()
        for i in range(0, len(grade_list)):
            print("取得成绩:%d 对应次数:%d" % (grade_list[i]['grade'], grade_list[i]['counts']))
        num_list = [0, 0, 0, 0, 0]
        label_list = ["0-59分", "60-69分", "70-79分", "80-89分", "90-100分"]
        color_list = ["royalblue","darkcyan","yellowgreen","yellow","orangered"]
        for i in range(len(grade_list)):
            grade = grade_list[i]['grade']
            if grade >= 0 and grade <= 59:
                num_list[0] += grade_list[i]['counts']
            elif grade >= 60 and grade <= 69:
                num_list[1] += grade_list[i]['counts']
            elif grade >= 70 and grade <= 79:
                num_list[2] += grade_list[i]['counts']
            elif grade >= 80 and grade <= 89:
                num_list[3] += grade_list[i]['counts']
            else:
                num_list[4] += grade_list[i]['counts']
        #柱状图
        plt.figure(figsize=(5,5))
        plt.title('直方图')
        plt.xlabel('分数段')
        plt.ylabel('计数')
        if max(num_list) <= 4:
            plt.yticks(list(range(max(num_list) + 1)))
        plt.bar(range(len(num_list)), num_list, color=color_list, tick_label=label_list)
        plt.savefig("static/teacher_stat_img/bar_" + teacher_id + '_' + course_id + ".jpg")  #图片拿教师id+课程id作为标识
        plt.close()
        #饼图
        #获得个数非0的成绩段（以及相应的label_list和color_list）
        pie_num_list, pie_label_list, pie_color_list = [], [], []
        for i in range(len(num_list)):
            if num_list[i] > 0:
                pie_num_list.append(num_list[i])
                pie_label_list.append(label_list[i])
                pie_color_list.append(color_list[i])
        plt.figure(figsize=(5.3, 5.3))
        plt.title('饼状图')
        plt.pie(pie_num_list, labels=pie_label_list, colors=pie_color_list, autopct='%1.2f%%', textprops={'fontsize':12,'color':'black'})
        plt.axis('equal')
        plt.savefig("static/teacher_stat_img/pie_" + teacher_id + '_' + course_id + ".jpg")#图片拿教师id+课程id作为标识
        plt.close()
        #将教师所教的全部课程信息、该课程所有学生成绩分布的数据、图片所在路径包装成一个字典返回给前端
        data = {}
        data["courseinfo"] = result_list
        data["gradeinfo"] = grade_list
        data["bar"] = "teacher_stat_img/bar_" + teacher_id + '_' + course_id + ".jpg"
        data["pie"] = "teacher_stat_img/pie_" + teacher_id + '_' + course_id + ".jpg"
        data["course_name"] = course_name
        return render(request, 'teacher4-2.html', data)
    else:
        print("用户身份不合法")
        return redirect('/pro/illegalUser/')