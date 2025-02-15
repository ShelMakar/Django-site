import django.contrib.admin
import django.utils.timezone

import feedback.models


class FeedbackContactInline(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackContact


class FeedbackFileInline(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackFile


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = [
        'get_contact_name',
        'status',
        'created_on',
    ]
    can_delete = False

    inlines = [FeedbackContactInline, FeedbackFileInline]

    def get_contact_name(self, obj):
        return obj.feedbacks.name if obj.feedbacks else '-'

    get_contact_name.short_description = 'Контакт'

    def save_model(self, request, obj, form, change):
        if change:
            previous = feedback.models.Feedback.objects.get(pk=obj.pk)
            if obj.status != previous.status:
                feedback.models.StatusLog.objects.create(
                    feedback=obj,
                    user=request.user,
                    from_status=previous.status,
                    to=obj.status,
                    timestamp=django.utils.timezone.now(),
                )

        super().save_model(request, obj, form, change)


@django.contrib.admin.register(feedback.models.StatusLog)
class StatusLogAdmin(django.contrib.admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'from_status', 'to']
    search_fields = ['feedback__name', 'from_status', 'to']
    list_filter = ['timestamp', 'from_status', 'to']


__all__ = ['FeedbackAdmin', 'StatusLogAdmin']
