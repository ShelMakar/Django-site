import django.forms
import django.contrib.auth.forms
import django.contrib.auth.models
from django import forms

import users.models


class SignupForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = django.contrib.auth.models.User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label="Почта", required=True)

    class Meta:
        model = users.models.Profile
        fields = [
            'image',
            'birthday',
        ]
        labels = {
            'image': 'Аватарка',
            'birthday': 'День рождения',
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = django.contrib.auth.models.User
        fields = [
            'first_name',
            'email',
            'last_name',
         ]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = users.models.Profile
        fields = [
            'image',
            'birthday',
        ]


class AuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    pass
