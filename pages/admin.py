from django.contrib import admin
from .models import Contact, FineDining, CustomisedDining, EmberDining

admin.site.register(FineDining)
admin.site.register(Contact)
admin.site.register(CustomisedDining)
admin.site.register(EmberDining)
