from django.contrib import admin
from .models import File

# Register your models here.

class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'downloads_count', 'emailed_count')
admin.site.register(File, FileAdmin)