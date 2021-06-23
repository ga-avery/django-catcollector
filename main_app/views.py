from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def about(request):
  return render(request, 'about.html')


def index(request):
  # return HttpResponse('<h1>/ᐠ｡‸｡ᐟ\\</h1>')
  return render(request, 'index.html')