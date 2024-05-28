from django.contrib import admin
from .models import Contact, FineDining, CustomisedDining

admin.site.register(FineDining)
admin.site.register(Contact)
admin.site.register(CustomisedDining)
