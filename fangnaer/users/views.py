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
    def list(self, request):
        return Response('post /wechat/login -  post /wechat/logout')

    @decorators.action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        print('666666666666')
        req_data = request.data
        wx_req_data = urlencode({
            "appid": "*",
            "secret": "*",
            "js_code": req_data['wx_code'],
            "grant_type": "authorization_code"
        })
        wx_request = requests.post(url="https://api.weixin.qq.com/sns/jscode2session", data=wx_req_data)
        wx_session = wx_request.text
        wx_session_reslut = WeChatOpenIdSerializer(data=json.loads(wx_session.read()))
        if wx_session_reslut.is_valid():
            openid = wx_session_reslut.data['openid']
            user, status = User.objects.get_or_create(username=openid)
            wechat_user, status = WeChatUser.objects.get_or_create(user=user,
                                                                   openid=openid)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': "登陆失败！"})

    @decorators.action(methods=['post'], detail=False)
    def logout(self, request, *args, **kwargs):
        pass