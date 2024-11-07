import django.conf
import django.db
import django.forms


def upload_to(instance, filename):
    return f'uploads/{instance.feedback.id}/{filename}'


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ('received', 'получено'),
        ('in_progress', 'в обработке'),
        ('answered', 'ответ дан'),
    ]

    text = django.db.models.TextField()
    created_on = django.db.models.DateTimeField(auto_now_add=True, null=True)
    status = django.db.models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received',
    )


class FeedbackContact(django.db.models.Model):
    name = django.db.models.CharField(max_length=100, null=True, blank=True)
    mail = django.db.models.EmailField()
    contact = django.db.models.ForeignKey(
        Feedback, related_name='feedbacks', on_delete=django.db.models.CASCADE,
    )


class FeedbackFile(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback, related_name='files', on_delete=django.db.models.CASCADE,
    )
    file = django.db.models.FileField(
        upload_to=upload_to,
        null=True,
        blank=True,
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
    from_status = django.db.models.CharField(max_length=20, db_column='from')
    to = django.db.models.CharField(max_length=100)


__all__ = ['Feedback', 'StatusLog']
