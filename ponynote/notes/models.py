from django.db import models
from django.contrib.auth.models import User
import ponynote.settings as settings
import os

class Note(models.Model):
    text = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE,
                              null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

def root_path(instance, filename):
    return os.path.join(
        settings.MEDIA_ROOT,
        instance.owner.username        
    )


# Folder model for virtual folders
class Folder(models.Model):
    #folder_path = models.CharField(max_length=300, primary_key=True)
    folder_name = models.CharField(max_length=300)
    owner = models.ForeignKey(User, related_name="dirs", on_delete=models.CASCADE)
    #parent_folder = models.CharField(max_length=300)
    parent_folder = models.ForeignKey('self', max_length=300, 
                                     related_name='dirs', null=True,
                                     on_delete=models.CASCADE)

def create_path(instance, filename):
    parent = instance.folder_path
    paths = []
    while parent:
        paths.append(parent.folder_name)
        parent = parent.parent_folder
    paths = paths[::-1]+[filename]
    return os.path.join(
        settings.MEDIA_ROOT,
        instance.owner.username,
        *paths
    )

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=create_path, null=True, max_length=255)
    file_name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name="files", on_delete=models.CASCADE,
                              null=True)
    folder_path = models.ForeignKey(Folder, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.file.name)