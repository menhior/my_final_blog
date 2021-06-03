from django.contrib import admin

from .models import ObjectViewed, UserFilter, UserSearch
# Register your models here.

admin.site.register(ObjectViewed)
admin.site.register(UserFilter)
admin.site.register(UserSearch)