from rest_framework import serializers
from backend.users.models import WeChatUser


class WeChatOpenIdSerializer(serializers.Serializer):
   openid = serializers.CharField()
   session_key = serializers.CharField()
   # expires_in = serializers.IntegerField()


class WeChatUserSerializer(serializers.ModelSerializer):

   class Meta:
       model = WeChatUser
       fields = ('__all__')
       # fields = ('nick_name', 'avatar_url', 'gender', 'city', 'province', 'country', 'language')
       read_only_fields = ('openid', 'user')
