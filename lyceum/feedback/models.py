import django.conf
import django.db
import django.forms


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

    class Meta:
        verbose_name = 'фидбек'
        verbose_name_plural = 'фидбеки'


class FeedbackContact(django.db.models.Model):
    name = django.db.models.CharField(max_length=100, null=True, blank=True)
    mail = django.db.models.EmailField()
    contact = django.db.models.OneToOneField(
        Feedback,
        related_name='feedbacks',
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'контакт фидбека'
        verbose_name_plural = 'контакты фидбека'


class FeedbackFile(django.db.models.Model):
    def upload_to(self, filename):
        return f'uploads/{self.feedback_id}/{filename}'

    feedback = django.db.models.ForeignKey(
        Feedback,
        related_name='files',
        on_delete=django.db.models.CASCADE,
        verbose_name='',
    )
    file = django.db.models.FileField(
        upload_to=upload_to,
        null=True,
        blank=True,
        verbose_name='',
    )

    class Meta:
        verbose_name = 'фидбек файл'
        verbose_name_plural = 'фидбек файлы'


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
        verbose_name='пользователь',
    )
    timestamp = django.db.models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='время изменения',
    )
    from_status = django.db.models.CharField(
        max_length=20,
        db_column='from',
        verbose_name='старый статус',
    )
    to = django.db.models.CharField(
        max_length=100,
        verbose_name='новый статус',
    )

    class Meta:
        verbose_name = 'лог статуса'
        verbose_name_plural = 'логи статуса'


__all__ = ['Feedback', 'StatusLog']
