from django.conf.urls import include, url
from rest_framework import routers

from .api import (NoteViewSet, RegistrationAPI, LoginAPI, 
                 UserAPI, FolderViewSet, FileUploadAPIView)

router = routers.DefaultRouter()
router.register('notes', NoteViewSet, 'notes')
router.register('dirs', FolderViewSet, 'dirs')
router.register('upload', FileUploadAPIView, 'upload')

urlpatterns = [
    url("^", include(router.urls)),
    url("^auth/register/$", RegistrationAPI.as_view()),
    url("^auth/login/$", LoginAPI.as_view()),
    url("^auth/user/$", UserAPI.as_view()),
]
