from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as user_views
from users.forms import AuthenticationForm


reg_uidb64 = '(?P<uidb64>[0-9A-Za-z_]+)'
reg_token = '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'

app_name = 'users'


auth_patterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            form_class=AuthenticationForm,
            template_name='users/login.html',
        ),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='users/logout.html',
        ),
        name='logout',
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]

user_patterns = [
    path('signup/', user_views.signup, name='signup'),
    path('profile/', user_views.profile_view, name='profile'),
    path('user_list/', user_views.user_list, name='user_list'),
    path('user_detail/<int:pk>/', user_views.user_detail, name='user_detail'),
    path(
        f'activate/{reg_uidb64}/{reg_token}/',
        user_views.activate,
        name='activate',
    ),
]

urlpatterns = auth_patterns + user_patterns
