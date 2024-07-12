from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    CustomLogoutView,
    LogoutConfirmView,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    AboutMeView,
    RegisterView,
    UploadAvatarAboutMeView,
    UploadAvatarView,
    UserListView,
    UserDetailView,
    UpdateUserView
)

app_name = "myauth"
urlpatterns = [
    path("", UserListView.as_view(), name="users"),
    path("login/", LoginView.as_view(
        template_name="myauth/login.html",
        redirect_authenticated_user=True,
    ), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("logout_confirm/", LogoutConfirmView.as_view(), name="logout_confirm"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UpdateUserView.as_view(), name="user_update"),
    path("upload-avatar_me/",UploadAvatarAboutMeView.as_view(), name="upload-avatar_me"),
    path("upload-avatar/", UploadAvatarView.as_view(), name="upload-avatar"),
    path("register/", RegisterView.as_view(), name="register"),
    path("cookie/get", get_cookie_view, name="cookie-get"),
    path("cookie/set", set_cookie_view, name="cookie-set"),
    path("session/get", get_session_view, name="session-get"),
    path("session/set", set_session_view, name="session-set"),
]
