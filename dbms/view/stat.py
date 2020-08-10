#统计子系统
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse

#学生成绩分布的统计函数
def indexSGPADIST(request):
    print("查询成绩分布")
    if 'sessionid' in request.COOKIES and request.session['role'] == 'student':
        connection.connect()
        cursor = connection.cursor()
        cursor.execute("select grade,count(grade) as counts\
                        from take\
                        where student_id=%s\
                        group by grade;",[request.session['id']])   #根据具体学生id查询成绩分布
        result_list=[]
        result = cursor.fetchone()
        tmp=('grade','counts')
        while result:
            result_list.append(dict(zip(tmp, result)))
            result = cursor.fetchone()
        for i in range(0, len(result_list)):
            print("取得成绩:%d 对应次数:%d" % (result_list[i]['grade'], result_list[i]['counts']))
        return redirect('/pro/student/')
    else:
        print("用户身份不合法")
        return redirect('/pro/login/')

#教师成绩分布的统计函数
def indexTDist(request):
    print("查询学生成绩分布")