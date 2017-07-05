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
    url(r'^gra/([a-zA-Z0-9]*)$',views.gra,name='gra'),
    url(r'^bin/([a-zA-Z0-9]*)$',views.bin,name='bin'),
    url(r'^gau/([a-zA-Z0-9]*)$',views.gau,name='gau'),
    url(r'^sca/([a-zA-Z0-9]*)$',views.sca,name='sca'),
    url(r'^rot/([a-zA-Z0-9]*)$',views.rot,name='rot'),
    url(r'^con/([a-zA-Z0-9]*)$',views.con,name='con'),
    url(r'^process/([a-zA-Z0-9]*)$', views.process, name='process'),
    url(r'^display/([\s\S]*)$', views.display, name='display'),
    url(r'^square$', views.square, name='square'),
    url(r'^like/([a-zA-Z0-9]*)$',views.like, name='like'),
    url(r'^save/([a-zA-Z0-9]*)$',views.save, name='save'),
    url(r'^unsave/([a-zA-Z0-9]*)$',views.unsave, name='unsave'),
    url(r'^savelist$', views.savelist, name='savelist'),
    url(r'^delpic/([a-zA-Z0-9]*)$',views.delpic, name='delpic'),
    url(r'^home/([0-9]*)$', views.home, name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
