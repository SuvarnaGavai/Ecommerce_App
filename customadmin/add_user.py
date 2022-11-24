from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.authki.models import User

from django import add_user
from django.forms import EmailInput, ModelForm, PasswordInput
from manager.models import Person


class RegisterForm(ModelForm):
    username = add_user.CharField(max_length=100)
    password = add_user.CharField(widget=PasswordInput)
    email = add_user.CharField(widget=EmailInput)
    discord_id = add_user.CharField(max_length=100, label='Discord ID')
    zoom_id = add_user.CharField(max_length=100, label='Zoom ID')

    class Meta:
        model = Person
        fields = ["username", "password", "birthdate", "email", "discord_id", "zoom_id"]
