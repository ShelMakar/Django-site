import django.contrib.auth.forms
from django.contrib.auth.models import User as User_model
import django.forms

import users.models


class UserChangeForm(django.forms.ModelForm):
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = User_model
        fields = [
            'first_name',
            'email',
            'last_name',
        ]


class SignupForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(max_length=200, help_text='Required')

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = User_model
        fields = [
            'username',
            'email',
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


class ProfileEditForm(django.forms.ModelForm):
    class Meta:
        model = users.models.Profile
        fields = [
            users.models.Profile.image.field.name,
            users.models.Profile.birthday.field.name,
            users.models.Profile.coffee_count.field.name,
        ]

    def __init__(self, *args, **kwargs):
        coffee = users.models.Profile.coffee_count.field.name
        super().__init__(*args, **kwargs)
        self.fields[coffee].disabled = (
            True,
        )


class AuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    pass


__all__ = []
