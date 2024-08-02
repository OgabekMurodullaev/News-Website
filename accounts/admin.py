from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'day_of_birth', 'image']


admin.site.register(Profile, ProfileAdmin)

