from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework import viewsets, decorators
import urllib, json
from urllib.parse import urlencode
from django.contrib.auth.models import User
from users.serializers import WeChatOpenIdSerializer, WeChatUserSerializer
from users.models import WeChatUser
import requests


class WeChatUserViewSet(viewsets.ViewSet):
    serializer_class = WeChatUserSerializer

    def list(self, request):
        return Response('post /member/update')

    @decorators.action(methods=['post'],  detail=False)
    def info(self, request, *args, **kwargs):
        wechat_user = WeChatUser.objects.get(user=request.user)
        serializer = self.serializer_class(wechat_user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WeChatAuthTokenViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer
    """
    微信认证
    """
    # def list(self, request):
    #     return Response('post /wechat/login -  post /wechat/logout')

    @decorators.action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        req_data = request.data
        wx_req_data = urlencode({
            "appid": "wxc0b94222c8840cba",
            "secret": "*",
            "js_code": req_data['code'],
            "grant_type": "authorization_code"
        })
        wx_request = requests.post(url="https://api.weixin.qq.com/sns/jscode2session", data=wx_req_data)
        wx_session = wx_request.text
        wx_session_reslut = json.loads(wx_session)
        response = {}
        if wx_session_reslut:
            openid = wx_session_reslut['openid']
            user, status = User.objects.get_or_create(username=openid)
            wechat_user, status = WeChatUser.objects.get_or_create(user=user,openid=openid)
            # token, created = Token.objects.get_or_create(user=user)
            response['openid'] = openid
            response['message'] = 'success'
            return JsonResponse(response)
        else:
            response['message'] = '登录失败'
            return Response(response)

    @decorators.action(methods=['post'], detail=True)
    def logout(self, request, *args, **kwargs):
        pass