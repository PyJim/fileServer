import os
from django.db import models


# create your models here

class File(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    path = models.URLField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True)
    downloads_count = models.IntegerField(default=0)
    emailed_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Automatically determine the file type based on file extension
        if self.path_or_url:
            _, file_extension = os.path.splitext(self.path_or_url)
            if file_extension:
                file_extension = file_extension.lower()
                if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    self.file_type = 'Image'
                elif file_extension in ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.xls', '.xlsx']:
                    self.file_type = 'Document'
                elif file_extension in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
                    self.file_type = 'Video'
                else:
                    self.file_type = 'Unknown'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
