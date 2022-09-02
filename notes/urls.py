from django.urls import path, include
from .views.views import UserDetailAPI, RegisterUserAPIView, NotesViewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"notes", NotesViewsets)

urlpatterns = [
    path("get-details", UserDetailAPI.as_view()),
    path("register", RegisterUserAPIView.as_view()),
    path("", include(router.urls)),
]
