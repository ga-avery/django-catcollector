from django.http.response import HttpResponse
from django.shortcuts import render
# Create your views here.
from .models import Cat, CatToy
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def about(request):
  return render(request, 'about.html')


def index(request):
  return render(request, 'index.html')


def cats_index(request):
  cats = Cat.objects.all()
  data = {'cats': cats}
  return render(request, 'cats/index.html', data)


def cat_show(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  return render(request, 'cats/show.html', {'cat': cat})


def profile(request, username):
  user = User.objects.get(username=username)
  cats = Cat.objects.filter(user=user)
  return render(request, 'profile.html', {'username': username, 'cats': cats})

class CatCreate(CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age', 'cattoys']
  success_url = '/cats'

  def form_valid(self, form) -> HttpResponse:
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect('/cats')
    


class CatUpdate(UpdateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age', 'cattoys']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect(f'/cats/{self.object.pk}')


class CatDelete(DeleteView):
  model = Cat
  fields = '/cats'
  success_url = '/cats'


def cattoys_index(request):
  cattoys = CatToy.objects.all()
  return render(request, 'cattoys/index.html', {'cattoys': cattoys})

def cattoys_show(request, cattoy_id):
  cattoy = CatToy.objects.get(id=cattoy_id)
  return render(request, 'cattoys/show.html', {'cattoy': cattoy})

class CatToyCreate(CreateView):
  model = CatToy
  fields = '__all__'
  success_url = '/cattoys'
  def form_valid(self, form) -> HttpResponse:
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect('/cattoys')
  pass
class CatToyUpdate(UpdateView):
  model = CatToy
  fields = ['name', 'color']
  success_url = '/cattoys'
  pass
class CatToyDelete(DeleteView):
  model = CatToy
  success_url = '/cattoys'
  pass
