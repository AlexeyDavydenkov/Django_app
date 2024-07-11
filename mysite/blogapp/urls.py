from django.urls import path
from .views import (
    BasedView,
    ArticleCreateView,
)

app_name = "blogapp"

urlpatterns = [
    path("", BasedView.as_view(), name="blogs"),
    path("create_blog/", ArticleCreateView.as_view(), name="create_blog"),
]
