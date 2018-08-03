"""fangnaer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from backend.users.views import WeChatAuthTokenViewSet
from backend.myapp.views import ThingsViewSet
from backend.myapp.views import show_media

router = routers.DefaultRouter()
router.register(r'v1', WeChatAuthTokenViewSet, base_name='wechat')
router.register(r'v1', ThingsViewSet, base_name='v1')


from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^', include(router.urls)),
    # url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/media/(?P<path_root>.*)$', show_media)
]