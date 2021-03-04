#coding=utf-8
# Create your views here.
from django.shortcuts import render,redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse


# Create your views here.
from django.http import  HttpResponse,HttpResponseRedirect

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #accept user input message
    post=request.POST
    uname=post.get('user_name')
    uemail=post.get('email')
    upwd1=post.get('pwd')
    upwd2=post.get('cpwd')
    #panduan database中是否有这个用户
    ''''user = UserInfo.objects.filter(uname=uname)
    if len(user)==1;
        
    else'''

    #if panduan   two password
    if upwd1==upwd2:
        #password jiami
        s1 = sha1()
        s1.update(upwd1.encode('utf-8'))
        upwd3 = s1.hexdigest()

        # create duixiang
        user = UserInfo()
        user.uname = uname
        user.upwd = upwd3
        user.uemail = uemail
        user.save()
        return redirect('/df_user/login')

    else:
        return redirect('/df_user/register')

def login(request):
    uname=request.COOKIES.get('uname','')
    context = {'title': '用户登陆', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    #accept web request data
    post=request.POST
    uusername=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)

    #根据用户名查询对象

    user = UserInfo.objects.filter(uname=uusername)
    print("1")
    # select * from userinfo where uname="uusername"
    # filter 和 get的区别？ 前者查不到不会抛异常，会抛出[]， 后者会抛异常， 这就是为啥下面用len(user)
    if len(user)==1:
        print("2")
        s1=sha1()
        s1.update(upwd.encode('utf-8'))
        #s2=s1.hexdigest()
        #s1.update(upwd)
        if s1.hexdigest()==user[0].upwd:
            print("7")
            #red=redirect('user_center_info')
            red = HttpResponseRedirect('info')
            #jizhu 用户名
            print("6")
            if jizhu!=0:
                red.set_cookie('uname',uusername)
            else:
                 red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=user[0].id
            request.session['user_name']=uusername
            print("5")
            return red
        else:
            context = {'title': '用户登陆', 'error_name':0,'error_pwd':1,'uname':uusername,'upwd':upwd}
            return render(request,'df_user/login.html',context)

    else:
        print("3")
        context = {'title': '用户登陆', 'error_name':1,'error_pwd':0,'uname':uusername,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    #select uemail from table where id='xxx';
    context={'title':'用户中心',
             'user_email':user_email,
             'user_name':request.session['user_name']}

    return render(request,'df_user/user_center_order.html',context)

def order(request):
    context={'title':'用户中心'}
    return render(request,'df_user/user_center_order.html',context)

def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context = {'title': '用户中心','user':user}
    return render(request,'df_user/user_center_site.html',context)

def register_exist(request):
    print("11")
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    #select count(*) from table where uname='xx'
    return JsonResponse({'count':count})

def index(request):
    return render(request,'../templates/index.html')

def center_info(request):
    print("4")
    return render(request,'df_user/user_center_info.html')


