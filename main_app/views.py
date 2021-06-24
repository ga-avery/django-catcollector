from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
from .models import Cat, CatToy


def about(request):
  return render(request, 'about.html')


def index(request):
  return render(request, 'index.html')

@login_required
def profile(request, username):
  user = User.objects.get(username=username)
  cats = Cat.objects.filter(user=user)
  return render(request, 'profile.html', {'username': username, 'cats': cats})


def cats_index(request):
  cats = Cat.objects.all()
  data = {'cats': cats}
  return render(request, 'cats/index.html', data)


def cat_show(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  return render(request, 'cats/show.html', {'cat': cat})


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


@method_decorator(login_required, name='dispatch')
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


def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)

    if not form.is_valid():
      print('-----------------------The username and/or password was incorrect')
      return HttpResponseRedirect('/login')

    u = form.cleaned_data['username']
    p = form.cleaned_data['password']
    user = authenticate(username=u, password=p)

    if not user.is_active:
      print('The account has been disabled')
      return HttpResponseRedirect('/login')

    login(request, user)
    return HttpResponseRedirect(f'/user/{u}')

  else:
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/cats')


def signup_view(request):
  if request.method is not 'POST':
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
  form = UserCreationForm(request.POST)
  if form.is_valid():
    user = form.save()
    login(request, user)
    return HttpResponseRedirect('/cats')
