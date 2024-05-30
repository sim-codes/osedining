from django.contrib import admin
from django.urls import re_path, path, include
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^\.well-known/', include('letsencrypt.urls')),
    re_path(r'^favicon\.ico$', favicon_view),
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('captcha/', include('captcha.urls')),
]
