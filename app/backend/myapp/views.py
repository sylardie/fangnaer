from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
from rest_framework import viewsets, decorators
from rest_framework.response import Response
from backend.myapp.models import Things
from backend.myapp.serializers import ThingsSerializer
from django.core.paginator import Paginator ,PageNotAnInteger ,EmptyPage


class ThingsViewSet(viewsets.ViewSet):
	serializer_class = ThingsSerializer

	@decorators.action(methods=['GET','POST', 'PATCH', 'DELETE'], detail=False)
	def thing(self, request, *args, **kwargs):
		# 新增
		response = {}
		if request.method == 'POST':
			if self.creator(request):
				response['msg'] = 'create_success'
				return JsonResponse(response)
			else:
				response['msg'] = 'create_fail'
				response['err_num'] = 0000
				return JsonResponse(response)
		# 查询
		elif request.method == 'GET':
			# 用request.META可以获取所有请求数据。根据需求提取。
			# print(request.META.keys())
			ret, page = self.filter(request)
			if ret:
				response['things_count'] = len(ret)
				response['list'] = ret
				response['msg'] = 'success'
				response['current_page'] = page
				return JsonResponse(response)
			else:
				response['things_count'] = len(ret)
				response['msg'] = 'success'
				response['list'] = []
				return JsonResponse(response)
		# 删除
		elif request.method == 'DELETE':
			if self.dele(request):
				response['msg'] = 'delete_success'
				return JsonResponse(response)
			else:
				response['msg'] = 'delete_fail'
				response['err_num'] = 2000
				return JsonResponse(response)
		# 更新
		elif request.method == 'PATCH':
			if self.update(request):
				response['msg'] = 'update_success'
				return JsonResponse(response)
			else:
				response['msg'] = 'update_fail'
				response['err_num'] = 3000
				return JsonResponse(response)

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

			paginator = Paginator(things, 5)
			# 把商品分成 5 个一页。
			try:
				thing_per_page = paginator.page(int(page))
			# 请求页数错误
			except PageNotAnInteger:
				thing_per_page = paginator.page(1)
			except EmptyPage:
				thing_per_page = paginator.page(paginator.num_pages)
			things_ser = ThingsSerializer(thing_per_page, many=True)
			return things_ser.data, thing_per_page.number
		else:
			return False

	def dele(self, request):
		user_id = request.META.get('HTTP_AUTHORIZATION')
		home = request.POST.get('home')
		thing_id = request.POST.get('id')
		print(thing_id, home)
		if user_id:
			if thing_id and not home:
				ret = Things.objects.filter(user=user_id, pk=thing_id).delete()
				print(ret)
				return True
			elif home and not thing_id:
				ret = Things.objects.filter(user=user_id, home=home).delete()
				print(ret)
				return True
			else:
				return False

	def update(self, request):
		user_id = request.META.get('HTTP_AUTHORIZATION')
		thing_id = request.POST.get('id')
		picture = request.FILES.get('picture')
		voice = request.FILES.get('voice')
		name = request.POST.get('name')
		home = request.POST.get('home')
		desc = request.POST.get('desc')
		if user_id:
			thing = Things.objects.get(pk=thing_id)
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


def show_media(request, path_root):
	'''
	这个地方注意URL的命名参数需要作为形参放到函数里
	'''
	local_path = os.path.join(os.path.dirname(os.path.abspath("__file__")), 'upload', path_root)

	with open(local_path, 'rb') as f:
		content = f.read()
	# 这里暂时只支持图片 TODO 音频返回
	return HttpResponse(content, content_type='image/png')



