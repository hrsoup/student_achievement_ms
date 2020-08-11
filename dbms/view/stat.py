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
        plt.title('成绩分布直方图')
        plt.xlabel('分数段')
        plt.ylabel('计数')
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
        plt.title('成绩分布饼状图')
        plt.pie(pie_num_list, labels=pie_label_list, colors=pie_color_list, autopct='%1.2f%%', textprops={'fontsize':12,'color':'black'})
        plt.axis('equal')
        plt.savefig("static/student_stat_img/pie_" + studentId + ".jpg")#图片拿学生id作为标识
        plt.close()
        #将具体数据和图片所在路径包装成一个字典返回给前端
        data = {}
        data["data"] = result_list
        data["bar"] = "student_stat_img/bar_" + studentId + ".jpg"
        data["pie"] = "student_stat_img/pie_" + studentId + ".jpg"
        return render(request, 'student4.html', data)
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

#教师成绩分布的统计函数
def indexTDist(request):
    print("查询学生成绩分布")
    return render(request, 'teacher4.html')