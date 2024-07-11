from django.urls import path
from .views import process_get_view, handle_file_upload

app_name = "requestdataapp"
urlpatterns = [
    path("get/", process_get_view, name="get-vew"),
    path("upload/", handle_file_upload, name="file-upload"),
]