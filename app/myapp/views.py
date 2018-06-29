from django.http import HttpResponse
from django.shortcuts import render
import os

# Create your views here.


def ssl_verify(request):
	with open(r'C:\Users\75318\Desktop\fangnaer\fileauth.txt', 'r', encoding='utf8') as f:
		content = f.read()
		print(content)

	return HttpResponse(content)
