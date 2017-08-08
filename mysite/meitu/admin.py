from django.contrib import admin
from .models import IMG, IMG_User, Like, Save, Invite, Remark

admin.site.register(IMG)
admin.site.register(IMG_User)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Invite)
admin.site.register(Remark)
# Register your models here.
