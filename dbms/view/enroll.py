#登录子系统，实现三种用户的登录/退出
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection

def welcome(request):
    #打印一下，做个示例
    if 'sessionid' not in request.COOKIES: #request.COOKIES是一个字典
        print("该用户没登录")
    else:
        print("该用户已经登录了")
    return render(request,'welcome.html')

def login(request):
    if(request.method == "POST"):
        connection.connect()    #开启连接
        cursor = connection.cursor()
        username = request.POST.get('username')
        password = request.POST.get('password')
        usertype = request.POST.get('my_select')
        if usertype == 'student':
            cursor.execute("select * from student where student_name='%s' and password='%s'" % (username,password)) #数据表中是否有该用户
            result = cursor.fetchall()
            connection.close()
            if len(result) == 0:
                obj = render(request,'login.html',status=400)
                if 'sessionid' in request.COOKIES:  #登陆失败时，如果cookie中有sessionid，就把它清除掉
                    request.session.flush() #清除一下对应的session
                    obj = render(request,'login.html',status=400)
                    obj.delete_cookie('sessionid')
                print("用户名或密码有问题，登录失败")
                return obj
            else:
                print("登录成功")
                request.session.flush() #清除一下之前的session
                #新创建一个session，设置该session的属性
                request.session['role'] = 'student' #用户类型
                request.session['id'] = result[0][0]    #用户唯一标识
                obj = redirect('/pro/student1')
                return obj
        elif usertype == 'teacher':
            cursor.execute("select * from teacher where teacher_name='%s' and password='%s'" % (username,password))
            result = cursor.fetchall()
            connection.close()
            print(result[0][0])
            if len(result) == 0:
                obj = render(request,'login.html',status=400)
                if 'sessionid' in request.COOKIES:
                    request.session.flush()
                    obj = render(request,'login.html',status=400)
                    obj.delete_cookie('sessionid')
                print("用户名或密码有问题，登录失败")
                return obj
            else:
                print("登录成功")
                request.session.flush()
                request.session['role']='teacher'
                request.session['id'] = result[0][0]
                obj = redirect('/pro/teacher1')
                return obj
        else:
            cursor.execute("select * from admin where admin_name='%s' and password='%s'" % (username,password))
            result = cursor.fetchall()
            connection.close()
            print(result[0][0])
            if len(result) == 0:
                obj = render(request,'login.html',status=400)
                if 'sessionid' in request.COOKIES:
                    request.session.flush()
                    obj = render(request,'login.html',status=400)
                    obj.delete_cookie('sessionid')
                print("用户名或密码有问题，登录失败")
                return obj
            else:
                print("登录成功")
                request.session.flush()
                request.session['role']='admin'
                request.session['id'] = result[0][0]
                obj = redirect('/pro/admin1')
                return obj
    else:
        return render(request,'login.html')