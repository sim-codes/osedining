from django.contrib import admin
from django.urls import re_path, path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    re_path(r'^\.well-known/', include('letsencrypt.urls')),
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('captcha/', include('captcha.urls')),
]
