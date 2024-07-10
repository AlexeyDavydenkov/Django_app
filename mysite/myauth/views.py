from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View, ListView, DetailView

from .models import Profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


class UserListView(ListView):
    model = User
    template_name = 'myauth/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'myauth/user_detail.html'
    context_object_name = 'user'


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


class LogoutConfirmView(TemplateView):
    template_name = "myauth/logout_confirm.html"


class UploadAvatarAboutMeView(View):
    def post(self, request, *args, **kwargs):
        avatar = request.FILES.get('avatar')
        if avatar:
            profile = request.user.profile
            profile.avatar = avatar
            profile.save()
        return redirect('myauth:about-me')


class UploadAvatarView(View):
    def post(self, request, *args, **kwargs):
        avatar = request.FILES.get('avatar')
        user_id = request.POST.get('user_id')
        if avatar and (request.user.is_staff or request.user.id == int(user_id)):
            profile = Profile.objects.get(user_id=user_id)
            profile.avatar = avatar
            profile.save()
        return redirect('myauth:user-detail', pk=user_id)


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookies set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default value")
    return HttpResponse(f"Session value: {value!r}")



