from django.contrib import admin
from django.contrib.auth.models import User

from users.models import Profile


class ProfileAdmin(admin.TabularInline):
    model = Profile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileAdmin]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
