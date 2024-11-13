import django.contrib.auth.forms
from django.contrib.auth.models import User as User_model
from django.db.models import Q
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
    email = django.forms.EmailField(
        max_length=200,
        help_text='Required',
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = User_model
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class ProfileForm(django.forms.ModelForm):
    email = django.forms.EmailField(
        label='Почта',
        required=True,
    )

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
        self.fields[coffee].disabled = (True,)


class AuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        ogg = User_model.objects.filter(
            Q(email=username) | Q(username=username),
        ).first()

        if ogg and password:
            self.user_cache = django.contrib.auth.authenticate(
                username=ogg.username, password=password,
            )
            if self.user_cache is None:
                raise django.forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


__all__ = []
