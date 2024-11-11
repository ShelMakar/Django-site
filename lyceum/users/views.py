from django.contrib.auth import get_user_model
import django.conf
from django.shortcuts import render, redirect
from .forms import SignupForm
import django.contrib.sites.shortcuts
import django.utils.http
import django.utils.encoding
import django.template.loader
from .token import account_activation_token
import django.core.mail
import django.http
import users.models
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

from .forms import UserEditForm, ProfileEditForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
            user.save()
            if not user.is_active:
                current_site = django.contrib.sites.shortcuts.get_current_site(
                    request
                )
                mail_subject = 'Activation link has been sent to your email id'
                message = django.template.loader.render_to_string(
                    'users/acc_active_email.html',
                    {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': django.utils.http.urlsafe_base64_encode(
                            django.utils.encoding.force_bytes(user.pk)
                        ),
                        'token': account_activation_token.make_token(user),
                    },
                )
                to_email = form.cleaned_data.get('email')
                email = django.core.mail.EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return django.http.HttpResponse(
                    'Please confirm your email address to complete the registration'
                )

            return django.http.HttpResponse(
                'Your account is active. You can now log in.'
            )
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    user = get_user_model()

    try:
        uid = django.utils.encoding.force_str(
            django.utils.http.urlsafe_base64_decode(uidb64)
        )
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        time_difference = (
            datetime.datetime.now(datetime.timezone.utc) - user.date_joined
        )
        if time_difference.total_seconds() <= 12 * 60 * 60:
            user.is_active = True
            user.save()
            return django.http.HttpResponse(
                'Thank you for your email confirmation. Now you can login your account.'
            )

        return django.http.HttpResponse(
            'Activation link has expired. Please sign up again.'
        )

    return django.http.HttpResponse('Activation link is invalid!')


def user_list(request):
    template = 'users/user_list.html'
    items = users.models.Profile.objects.filter(user__is_active=True).only(
        'image', 'user__username', 'birthday'
    )
    context = {'users': items}
    return django.shortcuts.render(request, template, context)


def user_detail(request, pk):
    template = 'users/user_detail.html'
    user = django.shortcuts.get_object_or_404(
        users.models.Profile.objects.filter(user__is_active=True).only(
            'image',
            'user__username',
            'user__first_name',
            'user__last_name',
            'birthday',
            'user__email',
            'coffee_count',
        ),
        pk=pk,
    )
    context = {'user': user}
    return django.shortcuts.render(request, template, context)


@login_required
def profile_view(request):
    profile = users.models.Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=profile, data=request.POST, files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(
        request,
        'users/profile.html',
        {'user_form': user_form, 'profile_form': profile_form},
    )
