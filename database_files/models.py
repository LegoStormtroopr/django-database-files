from django.db import models
from database_files.manager import FileManager


class FileInDatabase(models.Model):
    name = models.TextField(primary_key=True)
    size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.BinaryField()

    objects = FileManager()
