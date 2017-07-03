from django.conf.urls import url
from . import views, auth_views
from django.conf import  settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$', auth_views.index, name='index'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^signup$', auth_views.signup, name='signup'),
    url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^upload$', views.upload,name='upload'),
    url(r'^search$',views.search_img,name='search'),
    url(r'^gra/([a-zA-Z0-9]*)$',views.gra,name='gra'),
    url(r'^bin/([a-zA-Z0-9]*)$',views.bin,name='bin'),
    url(r'^gau/([a-zA-Z0-9]*)$',views.gau,name='gau'),
    url(r'^sca/([a-zA-Z0-9]*)$',views.sca,name='sca'),
    url(r'^rot/([a-zA-Z0-9]*)$',views.rot,name='rot'),
    url(r'^process/([a-zA-Z0-9]*)$', views.process, name='process'),
    url(r'^display/([\s\S]*)$', views.display, name='display'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
