from django.http import HttpResponse
from django.shortcuts import render
import os

from rest_framework import viewsets, decorators
from rest_framework.response import Response

from backend.myapp.models import Things
from backend.myapp.serializers import ThingsSerializer


class ThingsViewSet(viewsets.ViewSet):
	serializer_class = ThingsSerializer

	@decorators.action(methods=['GET','POST', 'PATCH', 'DELETE'], detail=False)
	def thing(self, request, *args, **kwargs):
		if request.method == 'POST':
			if self.creator(request):
				return HttpResponse('成功')
			else:
				return HttpResponse('失败')
		elif request.method == 'GET':
			# 用request.META可以获取所有请求数据。根据需求提取。
			# print(request.META.keys())
			ret = self.filter(request)
			if ret:
				return Response(ret)
			else:
				return Response('用户未授权')
		elif request.method == 'DELETE':
			return HttpResponse('DELETE')

	def creator(self, request):
		user_id = request.META.get('HTTP_AUTHORIZATION')
		picture = request.FILES.get('picture')
		voice = request.FILES.get('voice')
		name = request.POST.get('name')
		home = request.POST.get('home')
		desc = request.POST.get('desc')
		if user_id:
			thing = Things()
			thing.voice = voice
			thing.name = name
			thing.user = user_id
			thing.img = picture
			thing.desc = desc
			thing.home = home
			thing.save()
			return True
		else:
			print('用户未授权')
			return False

	def filter(self, request):
		user_id = request.META.get('HTTP_AUTHORIZATION')
		name = request.GET.get('name')
		home = request.GET.get('home')
		page = request.GET.get('page', 1)
		if user_id:
			if not name and not home:
				things = Things.objects.filter(user=user_id)
			elif name and not home:
				things = Things.objects.filter(name__icontains=name, user=user_id)
			elif home and not name:
				things = Things.objects.filter(home__icontains=home, user=user_id)
			else:
				things = Things.objects.filter(user=user_id)
			things_ser = ThingsSerializer(things, many=True)
			return things_ser.data
		else:
			print('用户未授权')
			return False






