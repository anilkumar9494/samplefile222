from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve 

from sport.views import android_file



urlpatterns = [

    path('admin/', admin.site.urls),
    path('dashboard/',include('dashboard.urls')),
    path('admin/clearcache/', include('clearcache.urls')),
    path('',include('sportapp.urls')),
    path('clientportal/',include('clientportal.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('api/v1/', include('apis.urls')),
    path('apk/',android_file,name="apk"),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

urlpatterns += i18n_patterns(

    path('dashboard/',include('dashboard.urls')),
    path('',include('sportapp.urls')),
    # path('clientportal/',include('clientportal.urls')),
    path('api/v1/', include('apis.urls')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
