import django.conf
import django.contrib.auth
import django.contrib.auth.decorators
import django.contrib.sites.shortcuts
import django.core.mail
import django.http
import django.shortcuts
import django.template.loader
import django.utils.encoding
import django.utils.http
import django.utils.timezone

import lyceum.settings
import users.forms
import users.models
import users.tokens


def signup(request):
    template = 'users/signup.html'
    if request.method == 'POST':

        form = users.forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = users.models.User.objects.normalize_email(user.email)
            user.is_active = lyceum.settings.DEFAULT_USER_IS_ACTIVE
            user.save()
            if not user.is_active:
                current_site = django.contrib.sites.shortcuts.get_current_site(
                    request,
                )
                mail_subject = 'Activation link has been sent to your email id'
                message = django.template.loader.render_to_string(
                    'users/acc_active_email.html',
                    {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': django.utils.http.urlsafe_base64_encode(
                            django.utils.encoding.force_bytes(user.pk),
                        ),
                        'token': users.tokens.activation_token.make_token(
                            user,
                        ),
                    },
                )
                to_email = form.cleaned_data.get('email')
                email = django.core.mail.EmailMessage(
                    mail_subject,
                    message,
                    to=[to_email],
                )
                email.send()
                return django.http.HttpResponse(
                    'Please confirm your email address '
                    'to complete the registration',
                )

            return django.http.HttpResponse(
                'Your account is active. You can now log in.',
            )
    else:
        form = users.forms.SignupForm()

    return django.shortcuts.render(request, template, {'form': form})


def activate(request, uidb64, token):
    user = django.contrib.auth.get_user_model()

    try:
        uid = django.utils.encoding.force_str(
            django.utils.http.urlsafe_base64_decode(uidb64),
        )
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and users.tokens.activation_token.check_token(
        user,
        token,
    ):
        if user.last_login is not None:
            time_difference = django.utils.timezone.now() - user.last_login
            if time_difference.total_seconds() <= 24 * 60 * 60 * 7:
                user.is_active = True
                user.save()
                return django.http.HttpResponse(
                    'Thank you for your email confirmation.'
                    ' Now you can login your account.',
                )
        elif user.date_joined is not None:
            time_difference = django.utils.timezone.now() - user.date_joined
            if time_difference.total_seconds() <= 12 * 60 * 60:
                user.is_active = True
                user.save()
                return django.http.HttpResponse(
                    'Thank you for your email confirmation.'
                    ' Now you can login your account.',
                )

        return django.http.HttpResponse(
            'Activation link has expired. Please sign up again.',
        )

    return django.http.HttpResponse('Activation link is invalid!')


def user_list(request):
    template = 'users/user_list.html'
    items = users.models.Profile.objects.filter(user__is_active=True).only(
        'image',
        'user__username',
        'birthday',
    )
    context = {'users': items}
    return django.shortcuts.render(request, template, context)


def user_detail(request, pk):
    template = 'users/user_detail.html'
    user_filter = users.models.Profile.objects.filter(
        user__is_active=True,
    ).only(
        'image',
        'user__username',
        'user__first_name',
        'user__last_name',
        'birthday',
        'user__email',
        'coffee_count',
    )
    user = django.shortcuts.get_object_or_404(
        user_filter,
        pk=pk,
    )
    context = {'user': user}
    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required
def profile_view(request):
    profile = users.models.Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = users.forms.UserChangeForm(
            instance=request.user,
            data=request.POST,
        )
        profile_form = users.forms.ProfileEditForm(
            instance=profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = users.forms.UserChangeForm(instance=request.user)
        profile_form = users.forms.ProfileEditForm(instance=profile)

    return django.shortcuts.render(
        request,
        'users/profile.html',
        {'user_form': user_form, 'profile_form': profile_form},
    )


__all__ = []
