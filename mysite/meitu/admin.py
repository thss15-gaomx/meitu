from django.contrib import admin
from .models import IMG, IMG_User, Like, Save, Invite

admin.site.register(IMG)
admin.site.register(IMG_User)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Invite)
# Register your models here.
