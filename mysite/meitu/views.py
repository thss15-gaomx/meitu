import os
from django.shortcuts import render
from itertools import chain
from .models import IMG
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.core.files.base import ContentFile
from .forms import UploadForm
import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from PIL import Image, ImageFilter
from django.db.models.fields.files import ImageFieldFile
import skimage.io

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            imgs = request.FILES.getlist('applyeruploadfile')
            for img in imgs:
                new_img = IMG()
                new_img.author = request.user
                new_img.category = form.cleaned_data['category']
                if form.cleaned_data['name']:
                    new_img.name = form.cleaned_data['name']
                else:
                    new_img.name = img.name
                new_img.content = img
                new_img.save()
                new_img.origin = new_img.id
                new_img.save()
                
                gra = IMG()
                gra.name = new_img.name
                gra.content = new_img.content
                gra.author = new_img.author
                gra.category = new_img.category
                gra.origin = new_img.id
                gra.is_ori = False
                gra.is_gra = True
                img_ori = Image.open(new_img.content)
                img_gra = img_ori.convert("L")
                img_gra.save('media/img/' + os.path.split(new_img.content.name)[-1] + 'gra.png')
                gra.content = ImageFieldFile(gra, gra.content, 'img/' + os.path.split(new_img.content.name)[-1] + 'gra.png')
                gra.save()
                
                sca = IMG()
                sca.name = new_img.name
                sca.content = new_img.content
                sca.author = new_img.author
                sca.category = new_img.category
                sca.origin = new_img.id
                sca.is_ori = False
                sca.is_sca = True
                (x, y) = img_ori.size
                img_sca = img_ori.resize((int(x/5), int(y/5)),Image.ANTIALIAS)
                img_sca.save('media/img/' + os.path.split(new_img.content.name)[-1] + 'sca.png')
                sca.content = ImageFieldFile(sca, sca.content, 'img/' + os.path.split(new_img.content.name)[-1] + 'sca.png')
                sca.save()
                
                bin = IMG()
                bin.name = new_img.name
                bin.content = new_img.content
                bin.author = new_img.author
                bin.category = new_img.category
                bin.origin = new_img.id
                bin.is_ori = False
                bin.is_bin = True
                ttt = np.mean(skimage.io.imread(new_img.content))
                img_bin = img_gra.point(lambda x: 255 if x > ttt else 0)
                img_bin = img_bin.convert('1')
                img_bin.save('media/img/' + os.path.split(new_img.content.name)[-1] + 'bin.png')
                bin.content = ImageFieldFile(bin, bin.content, 'img/' + os.path.split(new_img.content.name)[-1] + 'bin.png')
                bin.save()
        
                rot = IMG()
                rot.name = new_img.name
                rot.content = new_img.content
                rot.author = new_img.author
                rot.category = new_img.category
                rot.origin = new_img.id
                rot.is_ori = False
                rot.is_rot = True
                img_rot = img_ori.rotate(180)
                img_rot.save('media/img/' + os.path.split(new_img.content.name)[-1] + 'rot.png')
                rot.content = ImageFieldFile(rot, rot.content, 'img/' + os.path.split(new_img.content.name)[-1] + 'rot.png')
                rot.save()
        
                class MyGaussianBlur(ImageFilter.Filter):
                    name = "GaussianBlur"
    
                    def __init__(self, radius=2):
                        self.radius = radius
    
                    def filter(self, image):
                        return image.gaussian_blur(self.radius)

                gau = IMG()
                gau.name = new_img.name
                gau.content = new_img.content
                gau.author = new_img.author
                gau.category = new_img.category
                gau.origin = new_img.id
                gau.is_ori = False
                gau.is_gau = True
                img_gau = img_ori.filter(MyGaussianBlur(radius=3))
                img_gau.save('media/img/' + os.path.split(new_img.content.name)[-1] + 'gau.png')
                gau.content = ImageFieldFile(gau, gau.content, 'img/' + os.path.split(new_img.content.name)[-1] + 'gau.png')
                gau.save()
                
            return HttpResponseRedirect('/')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def search_img(request):
    return render(request,'search.html')

def process(request, number):
    pic = IMG.objects.filter(id=number)
    return render(request, "process.html", {'pictures': pic})

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
            pictures = IMG.objects.filter(author=request.user, category=cate, name=search_name)
        search_ori = True if request.POST.get('inlineCheckbox1') else False
        search_gra = True if request.POST.get('inlineCheckbox2') else False
        search_bin = True if request.POST.get('inlineCheckbox3') else False
        search_gau = True if request.POST.get('inlineCheckbox4') else False
        search_sca = True if request.POST.get('inlineCheckbox5') else False
        search_rot = True if request.POST.get('inlineCheckbox6') else False
    return render(request, "display.html", {'pictures': pictures,
                  'search_ori': search_ori, 'search_gra': search_gra, 'search_bin': search_bin,
                  'search_gau': search_gau, 'search_sca': search_sca, 'search_rot': search_rot})

def gra(request, number):
    pic1 = IMG.objects.filter(origin = number, is_ori = True)
    pic2 = IMG.objects.filter(origin = number, is_gra = True)
    pic = list(chain(pic1, pic2))
    return render(request, "process.html", {'pictures': pic})

def bin(request, number):
    pic1 = IMG.objects.filter(origin = number, is_ori = True)
    pic2 = IMG.objects.filter(origin = number, is_bin = True)
    pic = list(chain(pic1, pic2))
    return render(request, "process.html", {'pictures': pic})

def gau(request, number):
    pic1 = IMG.objects.filter(origin = number, is_ori = True)
    pic2 = IMG.objects.filter(origin = number, is_gau = True)
    pic = list(chain(pic1, pic2))
    return render(request, "process.html", {'pictures': pic})

def sca(request, number):
    pic1 = IMG.objects.filter(origin = number, is_ori = True)
    pic2 = IMG.objects.filter(origin = number, is_sca = True)
    pic = list(chain(pic1, pic2))
    return render(request, "process.html", {'pictures': pic})

def rot(request, number):
    pic1 = IMG.objects.filter(origin = number, is_ori = True)
    pic2 = IMG.objects.filter(origin = number, is_rot = True)
    pic = list(chain(pic1, pic2))
    return render(request, "process.html", {'pictures': pic})



