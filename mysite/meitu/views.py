import os
from django.shortcuts import render
from itertools import chain
from .models import IMG, IMG_User, Like, Save, Invite
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
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
                img_sca = img_ori.resize((int(x/2), int(y/2)),Image.ANTIALIAS)
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
                img_gau = img_ori.filter(MyGaussianBlur(radius=4))
                img_gau.save('media/img/' + os.path.split(new_img.content.name)[-1] + 'gau.png')
                gau.content = ImageFieldFile(gau, gau.content, 'img/' + os.path.split(new_img.content.name)[-1] + 'gau.png')
                gau.save()
                
                now_user = IMG_User.objects.get(u_id = request.user.id)
                if now_user.level > 4:
                    con = IMG()
                    con.name = new_img.name
                    con.content = new_img.content
                    con.author = new_img.author
                    con.category = new_img.category
                    con.origin = new_img.id
                    con.is_ori = False
                    con.is_con = True
                    img_con = img_ori.filter(ImageFilter.CONTOUR)
                    img_con.save('media/img/' + os.path.split(new_img.content.name)[-1] + 'con.png')
                    con.content = ImageFieldFile(con, con.content, 'img/' + os.path.split(new_img.content.name)[-1] + 'con.png')
                    con.save()
            
            return HttpResponseRedirect('/')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def process(request, number):
    pic = IMG.objects.filter(id=number)
    pic_author = IMG_User.objects.get(u_id = request.user.id)
    return render(request, "process.html", {'pictures': pic, 'pic_author':pic_author})

def display(request, cate):
    pic_user = IMG_User.objects.get(u_id = request.user.id)
    pictures = IMG.objects.filter(category=cate, author = request.user)
    search_ori = True
    search_gra = True
    search_bin = True
    search_gau = True
    search_sca = True
    search_rot = True
    search_con = True
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
        search_con = True if request.POST.get('inlineCheckbox7') else False
    return render(request, "display.html", {'pictures': pictures,
                  'search_ori': search_ori, 'search_gra': search_gra, 'search_bin': search_bin,
                  'search_gau': search_gau, 'search_sca': search_sca, 'search_rot': search_rot,
                  'search_con': search_con, 'pic_user': pic_user})

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

def con(request, number):
    pic1 = IMG.objects.filter(origin = number, is_ori = True)
    pic2 = IMG.objects.filter(origin = number, is_con = True)
    pic = list(chain(pic1, pic2))
    return render(request, "process.html", {'pictures': pic})

def square(request):
    pictures = IMG.objects.order_by('-uploaded_at')[0:100]
    pictures_top = IMG.objects.order_by('-liked_num')
    return render(request, "square.html", {'pictures': pictures, 'pic0': pictures_top[0], 'pic1': pictures_top[1], 'pic2': pictures_top[2]})

def like(request, pic_id):
    if not request.user.is_authenticated():
        return render(request, "login.html")
    pic = IMG.objects.get(id = pic_id)
    like = Like.objects.filter(fan = request.user, pic = pic)
    star = IMG_User.objects.get(u_id = pic.author.id)
    fan = IMG_User.objects.get(u_id = request.user.id)
    if like:
        pic.liked_num -= 1
        pic.save()
        like.delete()
        star.liked_num -= 1
        star.save()
        fan.like_num -= 1
        fan.save()
        return redirect('square')
    else:
        pic.liked_num += 1
        pic.save()
        new_like = Like()
        new_like.fan = request.user
        new_like.pic = pic
        new_like.save()
        star.liked_num += 1
        star.credit += 3
        star.save()
        star.level = (star.credit / 40) + 1
        star.save()
        star.storage = (star.level * 10) + 10
        star.save()
        fan.like_num += 1
        fan.credit += 1
        fan.save()
        fan.level = (fan.credit / 40) + 1
        fan.save()
        fan.storage = (fan.level * 10) + 10
        fan.save()
        return redirect('square')

def save(request, pic_id):
    if not request.user.is_authenticated():
        return render(request, "login.html")
    pic = IMG.objects.get(id=pic_id)
    star = IMG_User.objects.get(u_id = pic.author.id)
    fan = IMG_User.objects.get(u_id = request.user.id)
    if pic.author == request.user:
        messages.warning(request, '这是您自己上传的图片！')
    elif Save.objects.filter(fan = request.user, pic = pic):
        messages.warning(request, '您已收藏过该图片！')
    elif fan.storage <= fan.save_num:
        messages.warning(request, '您的收藏夹已满！')
    else:
        pic.saved_num += 1
        pic.save()
        new_save = Save()
        new_save.fan = request.user
        new_save.pic = pic
        new_save.save()
        messages.info(request, '收藏成功！')
        star.saved_num += 1
        star.credit += 3
        star.save()
        star.level = (star.credit // 40) + 1
        star.save()
        star.storage = (star.level * 10) + 10
        star.save()
        fan.save_num += 1
        fan.credit += 1
        fan.save()
        fan.level = (fan.credit // 40) + 1
        fan.save()
        fan.storage = (fan.level * 10) + 10
        fan.save()
    return redirect('square')

def savelist(request):
    if not request.user.is_authenticated():
        return render(request, "login.html")
    save_list = Save.objects.filter(fan=request.user)
    m_user = IMG_User.objects.filter(u_id = request.user.id)
    return render(request, "savelist.html", {'save_list':save_list, 'm_user':m_user})

def unsave(request, pic_id):
    pic = IMG.objects.get(id=pic_id)
    star = IMG_User.objects.get(u_id = pic.author.id)
    fan = IMG_User.objects.get(u_id = request.user.id)
    pic.saved_num -= 1
    pic.save()
    star.saved_num -= 1
    star.save()
    fan.save_num -= 1
    fan.save()
    unsave = Save.objects.get(fan=request.user,pic=pic)
    unsave.delete()
    return redirect('savelist')

