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
'''
    def index(request):
    posts=Post.objects.order_by('-created_at')
    return render(request,'index.html',{'posts':posts})
    '''
'''
    def show(request):
    pictures=Picture.objects.order_by('-uploaded_at')
    return render(request,'show.html',{'pictures':pictures})
    '''
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

def process_img(request):
    return render(request,'process.html')

def display(request, cate):
    pictures = IMG.objects.filter(category=cate)
    return render(request, "display.html", {'pictures': pictures})
