import django.contrib.admin
import django.utils.timezone

import feedback.models


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = [
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.status.field.name,
        feedback.models.Feedback.created_on.field.name,
    ]

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
