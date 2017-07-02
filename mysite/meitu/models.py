from django.db import models
from django.utils import timezone

# Create your models here.
class IMG(models.Model):
    author=models.ForeignKey('auth.User')
    content=models.ImageField(upload_to='img')
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    liked_num=models.IntegerField(default=0)
    uploaded_at=models.DateTimeField(default=timezone.now)
    is_ori=models.BooleanField(default=True)#是否是原图
    is_gra=models.BooleanField(default=False)#是否是灰度图
    is_bin=models.BooleanField(default=False)#是否二值化
    is_gau=models.BooleanField(default=False)#是否高斯平滑
    is_sca=models.BooleanField(default=False)#是否缩放
    is_rot=models.BooleanField(default=False)#是否旋转
