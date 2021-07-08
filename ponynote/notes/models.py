from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    text = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE,
                              null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

# Folder model for virtual folders
class Folder(models.Model):
    folder_path = models.CharField(max_length=300, primary_key=True)
    # foldername = models.CharField(max_length=20)
    owner = models.ForeignKey(User, related_name="dirs", on_delete=models.CASCADE)
    parent_folder = models.CharField(max_length=300)

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(null=True, max_length=255)
    owner = models.ForeignKey(User, related_name="files", on_delete=models.CASCADE,
                              null=True)
    folder_path = models.ForeignKey(Folder, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.file.name)