import django.contrib.admin
import django.contrib.auth.models

import users.models


class ProfileAdmin(django.contrib.admin.TabularInline):
    model = users.models.Profile
    can_delete = False
    readonly_fields = [users.models.Profile.coffee_count.field.name]


class UserAdmin(django.contrib.admin.ModelAdmin):
    inlines = [ProfileAdmin]


django.contrib.admin.site.unregister(django.contrib.auth.models.User)
django.contrib.admin.site.register(django.contrib.auth.models.User, UserAdmin)


__all__ = []
