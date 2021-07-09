from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from knox.models import AuthToken
from .models import Folder

from .serializers import (NoteSerializer, CreateUserSerializer,
                          UserSerializer, LoginUserSerializer,
                          MakeFolderSerializer, FileUploadSerializer)


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.request.user.notes.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = MakeFolderSerializer

    def get_queryset(self):
        return self.request.user.dirs.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# view for handling uploading of a file
class FileUploadAPIView(APIView):
    #authentication_classes = (permissions.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FileUploadSerializer

    def post(self, request):
        return self.create(request)

    def create(self, request):
        # print(request.data.get('folder_path'))
        folder = Folder.objects.get(folder_path=request.data.get('folder_path'))
        request.data['folder_path'] = folder
        serializer = self.serializer_class(data=request.data)
       # print(serializer)
        if serializer.is_valid(raise_exception=Response(status=400)):
            serializer.save()
            return Response(status=204)        


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # The Token.objects.create returns a tuple (instance, token). So in order 
            # to get token use the index 1
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # The Token.objects.create returns a tuple (instance, token). So in order 
            # to get token use the index 1
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
