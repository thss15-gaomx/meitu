from django.db import models
from django.utils import timezone

# Create your models here.
class IMG(models.Model):
    author=models.ForeignKey('auth.User')
    content=models.ImageField(upload_to='img')
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    liked_num=models.IntegerField(default=0)
    saved_num=models.IntegerField(default=0)
    uploaded_at=models.DateTimeField(default=timezone.now)
    origin = models.IntegerField(default=1)
    is_ori = models.BooleanField(default=True)#是否是原图
    is_gra = models.BooleanField(default=False)#是否是灰度图
    is_bin = models.BooleanField(default=False)#是否二值化
    is_gau = models.BooleanField(default=False)#是否高斯平滑
    is_sca = models.BooleanField(default=False)#是否缩放
    is_rot = models.BooleanField(default=False)#是否旋转
    is_con = models.BooleanField(default=False)#是否提取轮廓
    is_emb = models.BooleanField(default=False)#是否浮雕

class Like(models.Model):
    fan = models.ForeignKey('auth.User', null = True)
    pic = models.ForeignKey(IMG, null = True)

class Save(models.Model):
    fan = models.ForeignKey('auth.User', null = True)
    pic = models.ForeignKey(IMG, null = True)

class Invite(models.Model):
    from_id = models.IntegerField(default=0)
    to_id = models.IntegerField(default=0)

class IMG_User(models.Model):
    u_id = models.IntegerField(default = 0)
    like_num = models.IntegerField(default = 0)
    liked_num = models.IntegerField(default = 0)
    level = models.IntegerField(default = 1)
    credit = models.IntegerField(default = 0)
    storage = models.IntegerField(default = 60)
    pic_num = models.IntegerField(default = 0)
    saved_num = models.IntegerField(default = 0)
    save_num = models.IntegerField(default = 0)
    invite_num = models.IntegerField(default = 0)
    admin = models.BooleanField(default = False)

class Remark(models.Model):
    remarker = models.ForeignKey('auth.User', null = True)
    pic = models.ForeignKey(IMG, null = True)
    content = models.TextField(max_length=250)
    parent_comment_id = models.IntegerField(default = 0)
    remark_at=models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.remarker.username + ':' + self.content
