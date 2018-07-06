from django.db import models

from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class WeChatUser(models.Model):
    """"""
    Gender = (
        (0,'未知'),
        (1,'男'),
        (2,'女')
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    openid = models.CharField(max_length=253,verbose_name='微信openid')
    nick_name = models.CharField(max_length=253,verbose_name='昵称')
    avatar_url = models.CharField(max_length=253,verbose_name='用户头像')
    gender = models.CharField(max_length=253,verbose_name='性别',choices=Gender)
    # 用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
    city = models.CharField(max_length=253,verbose_name='所在城市')
    province = models.CharField(max_length=253,verbose_name='所在省份')
    country = models.CharField(max_length=253,verbose_name='所在国家')
    language = models.CharField(max_length=253,verbose_name='用户的语言')
    class Meta:
        verbose_name = "微信"
        verbose_name_plural = "微信"