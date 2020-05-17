#登录子系统，实现三种用户的登录/退出
from django.shortcuts import render,redirect
from django.http import HttpResponse

def welcome(request):
    return render(request,'welcome.html')

def login(request):
    if(request.method=="POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        usertype=request.POST.get('my_select')
        #打印用于调试
        print("login POST username:",username)
        print("login POST password:",password)
        print("login POST usertype:",usertype)
        if(usertype=='student'):
            return redirect('/pro/student1')
        elif(usertype=='teacher'):
            return redirect('/pro/teacher1')
        else:
            return redirect('/pro/admin1')
    else:
        return render(request,'login.html')