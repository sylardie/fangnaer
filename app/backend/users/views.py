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
import uuid
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
import time
from backend.users.redis_token import RUser


class WeChatAuthTokenViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer
    """
    微信认证
    """
    @decorators.action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        response = {}
        req_data = request.data
        print(request.data)
        wx_req_data = {"appid": "wxc0b94222c8840cba",
                       "secret": "f62b449568e2a8d07fd0728dfcbaf6b5",
                       "js_code": request.data['code']
        }

        # api = WXAPPAPI(appid="wxc0b94222c8840cba",
        #                app_secret="f62b449568e2a8d07fd0728dfcbaf6b5")
        # session_info = api.exchange_code_for_session_key(code=req_data['code'])
        # 获取session_info 后
        # session_key = session_info.get('session_key')
        # crypt = WXBizDataCrypt("wxc0b94222c8840cba", session_key)
        # # encrypted_data 包括敏感数据在内的完整用户信息的加密数据
        # # iv 加密算法的初始向量
        # # 这两个参数需要js获取
        # encrypted_data = req_data['encryptedData']
        # iv = req_data['iv']
        # user_info = crypt.decrypt(encrypted_data, iv)
        # openId = user_info['openId']
        # try:
        #     query_ret = WeChatUser.objects.get(openid=openId)
        # except Exception as e:
        #     u, status = User.objects.get_or_create(username=openId)
        #     user = WeChatUser()
        #     user.openid = openId
        #     user.user = u
        #     user.nick_name = user_info.get('nickName')
        #     user.gender = user_info.get('gender')
        #     user.language = user_info.get('language')
        #     user.city = user_info.get('province')
        #     user.country = user_info.get('country')
        #     user.avatar_url = user_info.get('avatarUrl')
        #     a_bool = user.save()
        #     print('cccc', a_bool)
        #     response['user'] = user_info
        #     return JsonResponse(response)
        # else:
        #     # 这里注意many后面的参数会影响.data的结果。
        #     query = WeChatUserSerializer(query_ret, many=False)
        #     print('eeee', query.data)
        #     response['user'] = query.data
        #     return JsonResponse(response)
        # TODO 用户缓存
        # except Exception as err:
        #     print(err)
        # return JsonResponse(response)

        wx_request = requests.post(url="https://api.weixin.qq.com/sns/jscode2session", data=wx_req_data)
        wx_session = wx_request.text
        wx_session_result = WeChatOpenIdSerializer(data=json.loads(wx_session))
        response = {}
        if wx_session_result.is_valid():
            print(wx_session_result.data)
            openid = wx_session_result.data['openid']
            session_key = wx_session_result.data['session_key']
            user, status = User.objects.get_or_create(username=openid)
            wechat_user, status = WeChatUser.objects.get_or_create(user=user, openid=openid)

            # 创建用户临时登陆态的唯一标识
            _token = str(uuid.uuid4())
            RUser.save_user_session(
                user_uuid=_token,
                openid=openid,
                session_key=session_key
            )

            response['_token'] = _token
            response['message'] = 'success'
            return Response(response)
        else:
            response['message'] = '登录失败'
            return Response(response)
