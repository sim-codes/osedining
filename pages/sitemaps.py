from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'

    priorities = {
        'pages:home': 1.0,
        'pages:ember_menu': 0.9,
        'pages:finedining': 0.8,
        'pages:menu': 0.8,
        'pages:customdining': 0.7,
        'pages:casual_dining': 0.7,
        'pages:hire_a_chef': 0.6,
        'pages:about': 0.6,
        'pages:gallery': 0.6,
        'pages:contact': 0.5,
    }

    def items(self):
        return list(self.priorities.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.priorities[item]
