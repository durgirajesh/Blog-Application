from django.contrib import admin
from .models import UserModel

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'password', 'createdAtDate', 'createdAtTime')

admin.site.register(UserModel, UserModelAdmin)
