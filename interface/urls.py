from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test, name="test_interface"),
    path("interface_test/", views.classify_test, name="classify"),
    path("classify/", views.upload_image, name="upload_image"),
]