from django.contrib import admin
from .models import User

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'password', 'createdAtDate', 'createdAtTime')

admin.site.register(User, UserModelAdmin)
