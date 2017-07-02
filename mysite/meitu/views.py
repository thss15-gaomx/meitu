from django.shortcuts import render
from .models import IMG
#from .forms import PictureForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.core.files.base import ContentFile
from .forms import UploadForm


def upload_img(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            imgs = request.FILES.getlist('applyeruploadfile')
            for img in imgs:
                new_img = IMG()
                new_img.author = request.user
                new_img.name = form.cleaned_data['name']
                new_img.category = form.cleaned_data['category']
                new_img.content = img
                new_img.save()
            return HttpResponseRedirect('/')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def search_img(request):
    return render(request,'search.html')

def process(request, number):
    pic = IMG.objects.filter(id=number)
    return render(request, "process.html", {'pictures': pic})
#return render(request,'process.html')

def display(request, cate):
    pictures = IMG.objects.filter(category=cate)
    search_ori = True
    search_gra = True
    search_bin = True
    search_gau = True
    search_sca = True
    search_rot = True
    if request.method == 'POST':
        search_name = request.POST.get('searchname')
        if search_name:
            pictures = IMG.objects.filter(category=cate, name=search_name)
        search_ori = True if request.POST.get('inlineCheckbox1') else False
        search_gra = True if request.POST.get('inlineCheckbox2') else False
        search_bin = True if request.POST.get('inlineCheckbox3') else False
        search_gau = True if request.POST.get('inlineCheckbox4') else False
        search_sca = True if request.POST.get('inlineCheckbox5') else False
        search_rot = True if request.POST.get('inlineCheckbox6') else False
    return render(request, "display.html", {'pictures': pictures,
                  'search_ori': search_ori, 'search_gra': search_gra, 'search_bin': search_bin,
                  'search_gau': search_gau, 'search_sca': search_sca, 'search_rot': search_rot})

def gra(request):
    pic = IMG.objects.all()
    return render(request, "process.html", {'pictures': pic})

def bin(request):
    pic = IMG.objects.all()
    return render(request, "process.html", {'pictures': pic})

def gau(request):
    pic = IMG.objects.all()
    return render(request, "process.html", {'pictures': pic})

def sca(request):
    pic = IMG.objects.all()
    return render(request, "process.html", {'pictures': pic})

def rot(request):
    pic = IMG.objects.all()
    return render(request, "process.html", {'pictures': pic})








