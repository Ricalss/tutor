from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lessons import models
import json
import requests
wxapp_ID = 'wx8fbdf2f847953186'
wxapp_secret = 'e4a2ada444f02fe99ef31aa3b705a013'

def viewsreturn(request, *args, **kwargs):
    return HttpResponse({"retinfoismine",2335201314})

@csrf_exempt
def retinfo(request):
    print(request)
    data = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 30},
        {'name': 'Charlie', 'age': 35}
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def tutor_tologin(request):
    if request.method == 'POST':
        wxapp_data = json.loads(request.body) # 小程序默认以json方式传递参数
        print(wxapp_data)
        if 'code'in wxapp_data :
            url = f'https://api.weixin.qq.com/sns/jscode2session?appid={wxapp_ID}&secret={wxapp_secret}&js_code={wxapp_data['code']}&grant_type=authorization_code'
            response = requests.get(url)
            data = response.json()
            print(data)
            if 'openid'in data:
                # 登录成功，处理用户信息等操作
                if models.user.objects.filter(openid=data['openid']):
                    retmsg = 'user already exists'
                else:
                    models.user.objects.create(openid = data['openid'])
                    retmsg = 'create new user'
                db = models.user.objects.filter(openid=data['openid']).values('id','name','gender','college','avatar')[0]
                print(db)
                #tokendata ={'userid':db,'name':"",'gender':"",'college':"",'avatarUrl':""}
                #return JsonResponse({'status': 'success', 'message':f'{retmsg }','token': {'openid':data['openid'],'session_key':data['session_key'],'islogin':'true'}})
                return JsonResponse({'status': 'success', 'message':f'{retmsg }','token': db})
            else:
                # 登录失败，返回错误信息
                return JsonResponse({'status': 'error', 'message': "Unable to get OpenID"})
        return JsonResponse({'status': 'error', 'message': "code isn't exist"})
    return JsonResponse({'status': 'error', 'message': "no code in POST"})
