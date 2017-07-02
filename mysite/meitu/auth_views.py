from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from .models import IMG

def index(request):
    if not request.user.is_authenticated():
        return render(request, "login.html")
    pictures = IMG.objects.all()
    cates = set()
    for c in pictures:
        cates.add(c.category)
    counter = {}.fromkeys(cates,0)
    for c in pictures:
        counter[c.category]+=1
    cate_list = []
    for key in counter:
        cate_list.append([key,counter[key]])
    cate_list.sort(reverse=True)
    return render(request, "index.html", {'pictures': pictures, 'cate_list':cate_list})

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, "login.html")
    else:
        return render(request, "login.html")

def signup(request):
    return render(request, 'signup.html')

def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    try:
       user = User.objects.create_user(username=username, password=password)
       return redirect('login')
    except:
       return redirect('signup')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')
