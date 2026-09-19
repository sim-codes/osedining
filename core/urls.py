from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import re_path, path, include
from django.views.generic.base import RedirectView, TemplateView

from pages.sitemaps import StaticViewSitemap

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    re_path(r'^\.well-known/', include('letsencrypt.urls')),
    re_path(r'^favicon\.ico$', favicon_view),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('', include('pages.urls')),
    path('captcha/', include('captcha.urls')),
]
