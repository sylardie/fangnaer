from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework import viewsets, decorators
import urllib, json
from urllib.parse import urlencode
from django.contrib.auth.models import User
from backend.users.serializers import WeChatOpenIdSerializer, WeChatUserSerializer
from backend.users.models import WeChatUser
import requests
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
import time
import redis


class WeChatAuthTokenViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer
    """
    微信认证
    """
    @decorators.action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        response = {}
        req_data = request.data
        api = WXAPPAPI(appid="wxc0b94222c8840cba",
                       app_secret="f62b449568e2a8d07fd0728dfcbaf6b5")
        session_info = api.exchange_code_for_session_key(code=req_data['code'])
        # 获取session_info 后
        session_key = session_info.get('session_key')
        crypt = WXBizDataCrypt("wxc0b94222c8840cba", session_key)
        # encrypted_data 包括敏感数据在内的完整用户信息的加密数据
        # iv 加密算法的初始向量
        # 这两个参数需要js获取
        encrypted_data = req_data['encryptedData']
        iv = req_data['iv']
        user_info = crypt.decrypt(encrypted_data, iv)
        openId = user_info['openId']
        try:
            query_ret = WeChatUser.objects.get(openid=openId)
        except Exception as e:
            u, status = User.objects.get_or_create(username=openId)
            user = WeChatUser()
            user.openid = openId
            user.user = u
            user.nick_name = user_info.get('nickName')
            user.gender = user_info.get('gender')
            user.language = user_info.get('language')
            user.city = user_info.get('province')
            user.country = user_info.get('country')
            user.avatar_url = user_info.get('avatarUrl')
            a_bool = user.save()
            print('cccc', a_bool)
            response['user'] = user_info
            return JsonResponse(response)
        else:
            # 这里注意many后面的参数会影响.data的结果。
            query = WeChatUserSerializer(query_ret, many=False)
            print('eeee', query.data)
            response['user'] = query.data
            return JsonResponse(response)
        # TODO 用户缓存
        # try:
        #     conn = redis.StrictRedis(host='127.0.0.1')
        #     conn.set('name', '蒋乐哥哥')
        #     conn.expire('name', 10)
        #     # 设置键的过期时间为10s
        #
        # except Exception as err:
        #     print(err)
        # return JsonResponse(response)

        # wx_request = requests.post(url="https://api.weixin.qq.com/sns/jscode2session", data=wx_req_data)
        # wx_session = wx_request.text
        # wx_session_reslut = WeChatOpenIdSerializer(data=json.loads(wx_session))
        # response = {}
        # if wx_session_reslut.is_valid():
        #     openid = wx_session_reslut.data['openid']
        #     user, status = User.objects.get_or_create(username=openid)
        #     wechat_user, status = WeChatUser.objects.get_or_create(user=user, openid=openid)
        #     response['openid'] = openid
        #     response['message'] = 'success'
        #     return Response(response)
        # else:
        #     response['message'] = '登录失败'
        #     return Response(response)
