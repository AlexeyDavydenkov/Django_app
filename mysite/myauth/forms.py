from django import forms
# from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from myauth.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "username", "first_name", "last_name", "email"
        # labels = {
        #     'name': _("Name"),
        #     'price': _("Price"),
        #     'description': _("Description"),
        #     'discount': _("Discount"),
        # }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "bio",