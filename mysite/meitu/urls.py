from django.conf.urls import url
from . import views, auth_views
from django.conf import  settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$', auth_views.index, name='index'),
    url(r'^login$', auth_views.login, name='login'),
    #url(r'^$',auth_views.login,name='login'),
    #url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
    url(r'^signup$', auth_views.signup, name='signup'),
    url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^upload$', views.upload_img,name='upload'),
    url(r'^search$',views.search_img,name='search'),
    url(r'^process$',views.process_img,name='process'),
    url(r'^display/([a-zA-Z0-9]*)$', views.display, name='display'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
