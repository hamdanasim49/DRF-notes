from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from notes.models.models import Notes
from ..serializers.serializers import NotesSerializer, UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, status, serializers
from rest_framework import permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
import json
from django.core import serializers
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from ..permissions.permissions import UserPermission

"""from .filters import NotesArchiveFilter"""


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class NotesViewsets(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    authentication_classes = (JWTAuthentication,)
    serializer_class = NotesSerializer
    permission_classes = [UserPermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["archive"]
    search_fields = ["text"]
    pagination_class = StandardResultsSetPagination
    """filter_class = NotesArchiveFilter"""

    def perform_create(self, serializer):
        print("Allo ***", self.request.user.username)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if "sharedWith" in data:
            note = self.queryset.get(pk=kwargs["pk"])
            idList = data["sharedWith"]

            for id in idList:
                id = int(id)
                curUser = User.objects.get(id=id)
                if id != self.request.user.id and curUser not in note.sharedWith.all():
                    note.sharedWith.add(curUser)

            noteS = NotesSerializer(note)
            return Response(noteS.data)

        else:
            return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["POST"], name="Archive-note")
    def archive(self, request, pk=None):
        queryset1 = self.queryset.all()
        note = queryset1.get(pk=pk)
        if note.archive:
            note.archive = False
        else:
            note.archive = True
        note.save()
        noteS = NotesSerializer(note)
        return Response(noteS.data)

    @action(detail=False, methods=["GET"], name="getShared")
    def shared(self, request):
        queryset = Notes.objects.all()
        curr_user = request.user
        queryset = queryset.filter(sharedWith=curr_user)
        data = serializers.serialize("json", queryset)
        return HttpResponse(data, content_type="application/json")
