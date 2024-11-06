import django.conf
import django.db
import django.forms


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ('received', 'получено'),
        ('in_progress', 'в обработке'),
        ('answered', 'ответ дан'),
    ]

    name = django.db.models.CharField(max_length=100, null=True, blank=True)
    text = django.db.models.TextField()
    created_on = django.db.models.DateTimeField(auto_now_add=True, null=True)
    mail = django.db.models.EmailField()
    status = django.db.models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received',
    )


class StatusLog(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        null=True,
        related_name='status_logs',
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
    )
    timestamp = django.db.models.DateTimeField(auto_now_add=True, null=True)
    from_status = django.db.models.CharField(max_length=20)
    to = django.db.models.CharField(max_length=100)


__all__ = ['Feedback', 'StatusLog']
