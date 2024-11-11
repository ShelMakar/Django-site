import django.contrib.auth.forms
from django.contrib.auth.models import User as User_model
import django.forms

import users.models


class SignupForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User_model
        fields = [
            User_model.username.field.name,
            User_model.email.field.name,
            'password1',
            'password2',
        ]


class ProfileForm(django.forms.ModelForm):
    email = django.forms.EmailField(label='Почта', required=True)

    class Meta:
        model = users.models.Profile
        fields = [
            users.models.Profile.image.field.name,
            users.models.Profile.birthday.field.name,
        ]
        labels = {
            'image': 'Аватарка',
            'birthday': 'День рождения',
        }


class UserEditForm(django.forms.ModelForm):
    class Meta:
        model = User_model
        fields = [
            User_model.first_name.field.name,
            User_model.email.field.name,
            User_model.last_name.field.name,
        ]


class ProfileEditForm(django.forms.ModelForm):
    class Meta:
        model = users.models.Profile
        fields = [
            users.models.Profile.image.field.name,
            users.models.Profile.birthday.field.name,
        ]


class AuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    pass


__all__ = []
