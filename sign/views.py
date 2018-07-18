# -*- coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest

# Create your views here.

def index(request):
    return render(request,'index.html')
#登录动作
def login_action(request):
    if request.method=="POST":
        username=request.POST.get("username","")
        password=request.POST.get("password","")
        # if username=="lan" and password=="123":
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user) #登录
            response=HttpResponseRedirect("/event_manage/")
            #response.set_cookie('user',username,3600) #添加浏览器cookie
            request.session['user']=username  #将session信息记录到浏览器中
            return response
        else:
            return render(request,"index.html",{"error":"password or username error"})

#发布会管理
@login_required
def event_manage(request):
    #username=request.COOKIES.get('user','') #读取浏览器cookie
    event_list=Event.objects.all()  #读取数据库数据
    #print event_list
    username=request.session.get('user','') #读取浏览器session
    return render(request,"event_manage.html",{"user":username,"events":event_list})

#发布会名称搜索
@login_required
def search_name(request):
    username=request.session.get('user','')
    search_name=request.GET.get("name","")
    event_list=Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#嘉宾管理
@login_required
def guest_manage(request):
    username=request.session.get('user','')
    guest_list=Guest.objects.all()
    return render(request,"guest_manage.html",{"user":username,"guest":guest_list})

#嘉宾按姓名搜索
@login_required
def search_realname(request):
    username=request.session.get('user','')
    search_name=request.GET.get("name","")
    guest_list=Guest.objects.filter(realname__contains=search_name)
    return render(request, "guest_manage.html", {"user": username, "guest": guest_list})

#签到页面
@login_required
def sign_index(request,eid):
    event=get_object_or_404(Event,id=eid)
    return render(request,"sign_index.html",{"event":event})


#签到动作
@login_required
def sign_index_action(request,eid):
    event=get_object_or_404(Event,id=eid)
    phone=request.POST.get("phone",'')
    result=Guest.objects.filter(phone=phone)
    if not result:
        return render(request,"sign_index.html",{"event":event,"hint":"phone is error"})
    result=Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,"sign_index.html",{"event":event,"hint":"event id or phone error"})
    result=Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,"sign_index.html",{"event":event,"hint":"user has sign in."})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,"sign_index.html",{"event":event,"hint":"sign in success","guest":result})

#退出系统
@login_required
def logout(request):
    auth.logout(request)
    response=HttpResponseRedirect('/index/')
    return response