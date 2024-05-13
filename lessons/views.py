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
            url = f"https://api.weixin.qq.com/sns/jscode2session?appid={wxapp_ID}&secret={wxapp_secret}&js_code={wxapp_data['code']}&grant_type=authorization_code"
            response = requests.get(url)
            data = response.json()  #data {'session_key': 'ixzZXN6RI/luRBOs2n0oKw==', 'openid': 'oz3gD7Q1eLGW9Bctqa9nlLPtxNuA'}
            print('微信服务器数据：',data)
            if 'openid'in data:
                # 登录成功，处理用户信息等操作
                if models.user.objects.filter(openid=data['openid']):
                    retmsg = 'user already exists'
                else:
                    if 'avatarUrl' not in wxapp_data or 'nickName' not in wxapp_data:
                        models.user.objects.create(openid = data['openid'])
                    else:
                        models.user.objects.create(openid = data['openid'],avatarUrl = wxapp_data['avatarUrl'],nickName=wxapp_data['nickName'])
                    retmsg = 'create new user'
                models.user.objects.filter(openid=data['openid']).update(session_key=data["session_key"])
                db = models.user.objects.filter(openid=data['openid']).values('id','user_type','name','gender','college','self_intro','avatarUrl','nickName')[0]
                print("db:",db)
                return JsonResponse({'status': 'success', 'message':f'{retmsg }','userinfo': db,'token':{'openid':data['openid'],'session_key':data['session_key'],'islogin':'true'}})
            else:
                # 登录失败，返回错误信息
                return JsonResponse({'status': 'error', 'message': "Unable to get OpenID"})
            
        elif((not wxapp_data['wxuser']) and 'id' not in wxapp_data):#app应用创建用户
            retid=models.user.objects.create(nickName=wxapp_data['nickName'],password=wxapp_data['password']).id #可能报错
            print(retid)
            retmsg = 'create new user'
            db = models.user.objects.filter(id=retid).values('id','user_type','name','gender','college','self_intro','avatarUrl','nickName')[0]
            print("db:",db)
            return JsonResponse({'status': 'success', 'message':f'{retmsg }','userinfo': db,'token':{'openid':'','session_key':'','islogin':'true'}})
        
        elif((not wxapp_data['wxuser']) and 'id' in wxapp_data):#app应用登录
            dbbuf = models.user.objects.filter(id=wxapp_data['id'])
            dbword=models.user.objects.filter(id=wxapp_data['id']).values('id','password')
            if(dbbuf):
                db = dbbuf.values('id','user_type','name','gender','college','self_intro','avatarUrl','nickName')[0]
                #print("db:",db)
                if(dbword[0]['password']==wxapp_data['password']):
                    return JsonResponse({'status': 'success', 'message':'log in !','userinfo': db,'token':{'openid':'','session_key':'','islogin':'true'}})
                else:
                    return JsonResponse({'status': 'pwdError', 'message':'password is wrong!'})
            else:
                return JsonResponse({'status': 'error', 'message':'user not found!'})

        return JsonResponse({'status': 'error', 'message': "code isn't exist"})
    return JsonResponse({'status': 'error', 'message': "no code in POST"})

@csrf_exempt
def tutor_changeuserinfo(request):
    if request.method == 'POST':
        wxappData = json.loads(request.body) # 小程序默认以json方式传递参数
        print(wxappData)
        wxInfo = wxappData['userinfo']
        models.user.objects.filter(id=wxInfo['id']).update(user_type=wxInfo["user_type"],name=wxInfo['name'],gender=wxInfo['gender'],college=wxInfo['college'],self_intro=wxInfo['self_intro'])
        dbRet = models.user.objects.filter(id=wxInfo['id']).values('id','user_type','name','gender','college','self_intro','avatarUrl','nickName')[0]
        print(dbRet)
        return JsonResponse({'status': 'success', 'message':'user info updated','userinfo':dbRet})
    return JsonResponse({'status': 'fail', 'message': "method should be POST"})

@csrf_exempt
def tutor_getpubmsg(request):
    if(request.method == 'POST'):
        wxappData = json.loads(request.body)
        print(wxappData)
        j=int(wxappData['msgNum'])+int(wxappData['msgIncrement'])
        dbRet=models.public_msg.objects.all().order_by('-id').values('userid','msg_type','timestamp','content')[0:j]
        msgRetNum = dbRet.count()
        print(dbRet)
        print(msgRetNum)  
        for item in dbRet:
            buf=models.user.objects.filter(id=item['userid']).values()[0]
            item['name']=buf['name']
        print(dbRet)
        return JsonResponse({'status': 'success', 'message': "return {}",'pubmsgShow':list(dbRet),'msgRetNum':msgRetNum})
    return JsonResponse({'status': 'fail', 'message': "method should be POST"})

@csrf_exempt
def tutor_pushPubmsg(request):
    if(request.method == 'POST'):
        wxappData = json.loads(request.body)
        print('wxappData:',wxappData)
        if('msg_type'in wxappData and 'userid'in wxappData and 'content'in wxappData):
            refUser = models.user.objects.filter(id=wxappData['userid'])[0]
            insertmsg=models.public_msg.objects.create(msg_type=wxappData['msg_type'],userid=refUser,content=wxappData['content'])
            print('insertmsg:',vars(insertmsg))
            if(insertmsg.id != 0):
                return JsonResponse({'status':'success','message':'pushed public msg'})
            else:
                return JsonResponse({'status': 'fail', 'message':'unable to insert into database'})
    return JsonResponse({'status': 'fail', 'message': "incorrect request!"})

@csrf_exempt
def tutor_lookuserUrl(request):
    if(request.method == 'POST'):
        wxData = json.loads(request.body)
        print('wxData:',wxData)
        if('lookuserid'in wxData):
            dbRet = models.user.objects.filter(id=wxData['lookuserid']).values('id','user_type','name','gender','college','self_intro','avatarUrl','nickName')[0]
            return JsonResponse({'status':'success','message':'get lookup user','lookuserinfo':dbRet})
    return JsonResponse({'status':'fail', 'message':'incorrect request'})


#微信小程序中this/that.data.var，需要有.data.
#"{{that.msgIncrement}}"小程序的json格式传输数据必须是字符串，django使用int（）转型
#queryset 是返回的一种list，整个list是queryset类型，切片也是queryset类型，但是list【i】是一个普通的字典