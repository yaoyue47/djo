import datetime
import json
from .module import re_email, captcha
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from shumeipai.models import User, Shumeipai, Main_data, System_inf, Shumeipai_limited


def index(request):
    if request.session.get("status", False):
        return redirect('shumeipai:home')
    else:
        return render(request, 'shumeipai/index.html')


def login(request):
    if request.method == 'GET':
        return HttpResponse('要用post哦')
    else:
        user = request.POST.get('user')
        check = request.POST.get("check")
        try:
            a = User.objects.get(user_name=user)
        except User.DoesNotExist:
            return HttpResponse('用户不存在')
        if a.password == request.POST.get('pwd'):
            request.session['status'] = True
            request.session['user'] = user
            if check != "on":
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('shumeipai:home')
        else:
            return HttpResponse('密码错误')


def login_ajax(request):  # ajax登录验证的接口 0为错1为对2验证码错误
    user = json.loads(request.body).get('user')
    pwd = json.loads(request.body).get('pwd')
    user_captcha = json.loads(request.body).get('captcha').lower()
    right_captcha = request.session.get('text').lower()
    try:
        a = User.objects.get(user_name=user)
    except User.DoesNotExist:
        return JsonResponse({'res': 0})
    if user_captcha != right_captcha:
        dit = {'res': 2}
    elif a.password != pwd:
        dit = {'res': 0}
    else:
        dit = {'res': 1}

    return JsonResponse(dit)


def home(request):
    if request.session.get('status', False):
        user = request.session.get('user')  # user是获取的用户名，str
        user_id = User.objects.get(user_name=user)
        shumeipai = user_id.shumeipai_set.all()  # shumeipai是和user_id有关的对象集
        shumeipai_name = []
        for i in shumeipai:
            shumeipai_name.append(i.name)
        shumeipai_getdata = request.GET.get('raspberry')
        set_cookie = False
        cookie_data = ''
        cookie_get = json.loads(request.COOKIES.get('raspberry'))
        if shumeipai_getdata and shumeipai_getdata in shumeipai_name:
            shumeipai_now = shumeipai_getdata
            set_cookie = True
            cookie_data = shumeipai_getdata
        elif cookie_get and cookie_get in shumeipai_name:
            shumeipai_now = cookie_get
        else:
            shumeipai_now = shumeipai_name[0]
            set_cookie = True
            cookie_data = shumeipai_name[0]
        click_time_db = System_inf.objects.get(pk=1)
        click_time = click_time_db.click_time + 1
        click_time_db.click_time = click_time
        click_time_db.save()
        render_data = {
            'user': user,
            'shumeipai': shumeipai_name,
            'shumeipai_now': shumeipai_now,
            'click_time': click_time
        }
        response = render(request, 'shumeipai/home.html', render_data)
        if set_cookie:
            response.set_cookie("raspberry", json.dumps(cookie_data), 60 * 60 * 24 * 7)
        return response
    else:
        return redirect('shumeipai:index')


def logout(request):
    request.session['status'] = False
    return redirect('shumeipai:index')


@csrf_exempt
def get_excel_data(request):  # 接受数据：page(int),shumeipai_name(str)
    hang = request.GET.get('hang', 6)
    page = request.GET.get('page', '1')
    page = int(page)
    shumeipai_name = request.GET.get("shumeipai_name", None)
    shumeipai = Shumeipai.objects.get(name=shumeipai_name)
    data = shumeipai.main_data_set.order_by("-id")[(page - 1) * hang:hang + 1 + (page - 1) * hang]
    return_data = []
    for i in data:
        creat_object = {"id": i.id, 'time': i.datetime.strftime('%Y-%m-%d %H:%M:%S'), 'temperature': i.temperature,
                        'humidity': i.humidity, 'ph': i.ph, 'sun': i.sun}
        return_data.append(creat_object)
    return JsonResponse(return_data, safe=False)


# 接口文档： 接受请求：page(str),shumeipai_name(str),hang(str)(可不写，默认6)  返回数据：[{"id": 2, "time": "2020-04-20T11:54:43.137Z",
# "temperature": 20.25, "humidity": 32.52}, {"id": 1, "time": "2020-04-20T11:54:24.658Z", "temperature": 20.21,
# "humidity": 25.32}]
@csrf_exempt
def get_echarts_data(request):
    tianshu = request.GET.get("tianshu")
    shumeipai_name = request.GET.get('shumeipai_name')
    shumeipai = Shumeipai.objects.get(name=shumeipai_name)
    if tianshu == '1':
        data = shumeipai.main_data_set.order_by('-id')[:48:4]  # 查询1天 有12条
    elif tianshu == '3':
        data = shumeipai.main_data_set.order_by('-id')[:144:16]  # 查询3天 有 9条
    elif tianshu == '7':
        data = shumeipai.main_data_set.order_by('-id')[:336:24]  # 查询7天 有14条
    else:
        return HttpResponse("格式出错")
    return_data = {
        "time": [],
        "temperature": [],
        "humidity": [],
        "ph": [],
        "sun": []
    }
    for i in data:
        return_data['time'].append(i.datetime.strftime('%y-%m-%d %H:%M:%S'))
        return_data['temperature'].append(i.temperature)
        return_data['humidity'].append(i.humidity)
        return_data['ph'].append(i.ph)
        return_data['sun'].append(i.sun)
    return_data["time"].reverse()
    return_data["temperature"].reverse()
    return_data["humidity"].reverse()
    return_data["ph"].reverse()
    return_data["sun"].reverse()
    return JsonResponse(return_data)
    # 接口文档：接受请求：tianshu：(str)("1",'3','7') shumeipai_name(str) 返回数据：{"time": ["20-04-24 19:47:12", "20-04-24
    # 01:49:01", "20-04-20 11:55:03"], "temperature": [10.01, 13.78, 22.21], "humidity": [21.16, 11.46, 42.92]}


def search(request):
    try:
        date_str = request.POST.get('input_date')
        if date_str == "":
            return render(request, 'shumeipai/search.html', {"date_json": []})
        user = request.session['user']
        shumeipai = json.loads(request.COOKIES['raspberry'])
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        user_db = User.objects.get(user_name=user)
        shumeipai_db = user_db.shumeipai_set.get(name=shumeipai)
        date_db = shumeipai_db.main_data_set.filter(datetime__year=date.year).filter(datetime__month=date.month).filter(
            datetime__day=date.day).values()
        date_json = list(date_db)
        return render(request, 'shumeipai/search.html', {"date_json": date_json})
    except:
        return HttpResponse("不支持直接访问！")


@csrf_exempt
def search_delete_update(request):  # 0为错1为对
    if request.method == "DELETE":
        id = json.loads(request.body).get("id")
        try:
            Main_data.objects.get(id=id).delete()
            return HttpResponse("1")
        except:
            return HttpResponse("0")
    elif request.method == 'POST':
        tem = request.POST.get("temperature")
        tem_f = round(float(tem), 2)
        hum = request.POST.get("humidity")
        hum_f = round(float(hum), 2)
        ph = request.POST.get("ph")
        ph_f = round(float(ph), 1)
        sun = request.POST.get("sun")
        sun_f = round(float(sun), 1)
        id = request.POST.get("id")
        try:
            Main_data.objects.filter(id=id).update(temperature=tem_f, humidity=hum_f, ph=ph_f, sun=sun_f)
            return HttpResponse("1")
        except:
            return HttpResponse("0")
    else:
        return HttpResponse("请求错误")


def configure(request):
    if request.method == "POST":
        user = request.POST.get("user")
        user_db = User.objects.get(user_name=user)
        shumeipai_db = user_db.shumeipai_set.values()
        shumeipai_list = list(shumeipai_db)
        return render(request, "shumeipai/configure.html", {"shumeipai": shumeipai_list, "user": user})
    else:
        return HttpResponse("不支持get请求")


@csrf_exempt  # 0为错1为对
def configure_delete(request):
    if request.method == "POST":
        shumeipai_id = request.POST.get('id')
        try:
            Shumeipai.objects.filter(id=shumeipai_id).delete()
            return HttpResponse("1")
        except:
            return HttpResponse("0")

    else:
        return HttpResponse("不支持get请求")


@csrf_exempt
def configure_update(request):  # 0为错1为对
    if request.method == "POST":
        shumeipai_id = request.POST.get("id")
        shumeipai_remarks = request.POST.get("remarks")
        try:
            shumeipai_db = Shumeipai.objects.get(id=shumeipai_id)
            shumeipai_db.remarks = shumeipai_remarks
            shumeipai_db.save()
            return HttpResponse("1")
        except:
            return HttpResponse('0')
    else:
        return HttpResponse("不支持get请求")


@csrf_exempt  # 0为错1为对
def configure_insert(request):
    if request.method == "POST":
        user = request.POST.get('user')
        name = request.POST.get("name")
        remarks = request.POST.get('remarks')
        try:
            user_db = User.objects.get(user_name=user)
            shumeipai_db = user_db.shumeipai_set.create(name=name, remarks=remarks)
            Shumeipai_limited.objects.create(shumeipai=shumeipai_db)
            return HttpResponse("1")
        except:
            return HttpResponse("0")
    else:
        return HttpResponse("不支持get请求")


def register(request):
    return render(request, 'shumeipai/register.html')


@csrf_exempt  # 0 正确 1邮箱格式 2用户名错误 3节点名字错误 4未知错误
def register_ajax(request):
    if request.method == "POST":
        user = json.loads(request.body).get("user")
        pwd = json.loads(request.body).get("pwd")
        name = json.loads(request.body).get("name")
        email = json.loads(request.body).get("email")
        if re_email.validateEmail(email) == '0':
            return HttpResponse("1")
        if User.objects.filter(user_name=user):
            return HttpResponse("2")
        if Shumeipai.objects.filter(name=name):
            return HttpResponse("3")
        try:
            user_db = User.objects.create(user_name=user, password=pwd, email=email)
            shumeipai_db = user_db.shumeipai_set.create(name=name)
            Shumeipai_limited.objects.create(shumeipai=shumeipai_db)
            return HttpResponse("0")
        except:
            return HttpResponse("4")
    else:
        return HttpResponse("不支持get访问")


def captcha_(request):
    captcha_object = captcha.captcha()
    text = captcha_object.run()  # 得到当前生成验证码图片内容
    request.session['text'] = text  # 传递正确的验证码，用于判断
    imagepath = "captcha.png"  # 存储验证码 图片 的路径
    image_data = open(imagepath, "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")


@csrf_exempt
def insert_data(request):
    if request.method == "POST":
        user = json.loads(request.body).get("user")
        shumeipai = json.loads(request.body).get("shumeipai")
        shumeipai_id = json.loads(request.body).get("shumeipai_id")
        tem = json.loads(request.body).get("tem")
        tem_f = round(float(tem), 2)
        hum = json.loads(request.body).get("hum")
        hum_f = round(float(hum), 2)
        ph = json.loads(request.body).get("ph")
        ph_f = round(float(ph), 1)
        sun = json.loads(request.body).get("sun")
        sun_f = round(float(sun), 1)
        if user and shumeipai and shumeipai_id and tem and hum and ph and sun:
            try:
                user_db = User.objects.get(user_name=user)
                shumeipai_db = user_db.shumeipai_set.get(pk=shumeipai_id)
            except:
                return HttpResponse("用户或者节点名称不存在!")
            if shumeipai_db.name == shumeipai:
                shumeipai_db.main_data_set.create(temperature=tem_f, humidity=hum_f, ph=ph_f, sun=sun_f)
                shumeipai_limited_db = shumeipai_db.shumeipai_limited.__dict__
                a = [{'value': tem_f, 'max': 'tem_max', 'min': 'tem_min', 'inf': '温度'},
                     {'value': hum_f, 'max': 'hum_max', 'min': 'hum_min', 'inf': '湿度'},
                     {'value': ph_f, 'max': 'ph_max', 'min': 'ph_min', 'inf': "ph"},
                     {'value': sun_f, 'max': 'sun_max', 'min': 'sun_min', 'inf': "光照强度"}]
                message = ''
                for i in a:
                    if i['value'] > shumeipai_limited_db[i['max']]:
                        message += shumeipai + '节点处' + i['inf'] + '过高!,请及时处理\n'
                    if i['value'] < shumeipai_limited_db[i['min']]:
                        message += shumeipai + '节点处' + i['inf'] + '过低!,请及时处理\n'
                if message != '':
                    shumeipai_db.status = False
                    shumeipai_db.save()
                    try:
                        send_mail("节点警告!", message, "2359240697@qq.com", ['2359240697@qq.com'])
                    except:
                        print('发送邮箱失败')
                else:
                    shumeipai_db.status = True
                    shumeipai_db.save()
                return HttpResponse("成功")
            else:
                return HttpResponse("验证失败!")
        else:
            return HttpResponse('格式错误!')
    else:
        return HttpResponse("请使用post请求!")

# 接口文档:
# 接受数据:user,shumeipai,shumeipai_id,tem,hum,ph,sun
# 返回数据:字符串
