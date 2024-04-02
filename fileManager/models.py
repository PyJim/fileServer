import os
from django.db import models


class File(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/', default='')
    date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True)
    downloads_count = models.IntegerField(default=0)
    emailed_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Set the path attribute to the URL of the uploaded file
        self.path = self.file.url

        # Automatically determine the file type based on file extension
        _, file_extension = os.path.splitext(self.file.name)
        if file_extension:
            file_extension = file_extension.lower()
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                self.file_type = 'image'
            elif file_extension in ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.xls', '.xlsx', '.csv']:
                self.file_type = 'document'
            elif file_extension in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
                self.file_type = 'video'
            else:
                self.file_type = 'unknown'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
