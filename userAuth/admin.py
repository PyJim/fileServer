from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_email_verified', 'last_login', 'date_joined')

admin.site.register(User, UserAdmin)