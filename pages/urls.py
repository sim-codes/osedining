from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('gallery/', views.GalleryPageView.as_view(), name='gallery'),
    path('finedining/', views.FineDiningView.as_view(), name='finedining'),
    path('ember-menu/', views.EmberMenuView.as_view(), name='ember_menu'),
    path('ember-menu/successful/', views.EmberMenuSuccessful.as_view(), name='ember_menu_success'),
    path('ember-menu/invoice/', views.EmberInvoicePreview.as_view(), name='ember_invoice_preview'),
    path('custom-dining/', views.CustomDiningView.as_view(), name='customdining'),
    path('hire-a-chef/', views.HireAChefView.as_view(), name='hire_a_chef'),
    path('hire-a-chef/successful', views.HireAChefSuccessfulView.as_view(), name='hire_a_chef_success'),
    path('custom-dining/successful/', views.CustomDiningSuccessView.as_view(), name='customdining-successful'),
    path('finedining/successful/', views.FineDiningSuccessful.as_view(), name='finedining_success'),
    path('casual-dining/', views.CasualDiningView.as_view(), name='casual_dining'),
    path('casual-dining/successful/', views.CasualDiningSuccessfulView.as_view(), name='casual_dining_success'),
    # path('reserve/', views.make_reservation, name='reserve')
]
