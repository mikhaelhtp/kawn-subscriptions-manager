from ast import Delete
from multiprocessing import Value
from optparse import Values
from pyexpat import model
from unicodedata import name
from urllib import request
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()

class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User

class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

class UsersAddForm(UserAdminCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """
    name = forms.CharField(max_length=255)
    username = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "name", "email", "type", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class UsersEditForm(ModelForm):
    class Meta:
        model = User
        fields = ["name", "email", "username", "type"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


# class UserInviteForm(forms.Form):
#     to = forms.EmailField(required=True)
#     subject = forms.CharField(required=True)
#     message = forms.CharField(widget=forms.Textarea, required=True)