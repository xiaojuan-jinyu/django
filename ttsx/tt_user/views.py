#coding:utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from models import UserInfo
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect,HttpResponse
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from decorators import *


# Create your views here.
def index(request):
    return render(request, 'tt_user/index.html')
def register(request):
    context = {'title':'天天生鲜-注册','top':'0'}
    return render(request,'tt_user/register.html',context)

def register_handle(request):
    dict = request.POST
    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    ucpwd = dict.get('cpwd')
    uemil = dict.get('email')

    if upwd != ucpwd:
        return redirect('/user/register/')

    s=sha1()
    s.update(upwd)
    upwd_sha1 = s.hexdigest()

    userinfo = UserInfo()
    userinfo.uname = uname
    userinfo.upwd = upwd_sha1
    userinfo.uemil = uemil
    userinfo.save()

    return redirect('/user/login/')

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'天天生鲜-登陆','uname':uname,'top':'0'}
    return render(request,'tt_user/login.html',context)

def check_user_name(request,name):
    data = UserInfo.objects.filter(uname=name).exists()
    return JsonResponse({'data':data})

def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def check_login(request):
    dict = request.POST
    username = dict.get('username')
    userpwd = dict.get('pwd')
    yzm = dict.get('yzm')
    verifycode = request.session['verifycode']
    checkbox = dict.get('checkbox')


    s = sha1()
    s.update(userpwd)
    pwd = s.hexdigest()
    if yzm != verifycode:
        return render(request,'tt_user/login.html',{'yzmerror':True,'top':'0'})
    if UserInfo.objects.filter(uname=username).exists():
        if pwd == UserInfo.objects.get(uname=username).upwd :
            path = request.session.get('url_path','/user/')
            request.session['uname'] = username
            if checkbox == 'on':
                request.session[username] = userpwd
                response = HttpResponseRedirect(path)
                response.set_cookie('uname',username,max_age=60*60*24*20)
                return response
            return redirect(path)
    return render(request,'tt_user/login.html',{'error':True,'top':'0'})

def session(request,name):
    # request.session.flush()
    h1=request.session.get(name)
    return JsonResponse({'data':h1})

# @decorators
def user_center_info(request):
    uname = request.session.get('uname')
    context = {'uname':uname,'login':True,'title':'天天生鲜-用户中心'}
    return render(request,'tt_user/user_center_info.html',context)

@decorators
def site(request):
    uname = request.session.get('uname')
    user = UserInfo.objects.get(uname=uname)
    if request.method == 'POST':
        dict = request.POST
        user.ushou = dict.get('shou')
        user.uaddress = dict.get('add')
        user.uphone = dict.get('tel')
        user.save()
    context = {'title':'收货地址','user':user}
    return render(request,'tt_user/user_center_site.html',context)

def quit(request):
    request.session.flush()
    return redirect('/user/login/')

