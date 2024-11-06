# Generated by Django 4.2.16 on 2024-11-06 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='status',
            field=models.CharField(
                choices=[
                    ('received', 'получено'),
                    ('in_progress', 'в обработке'),
                    ('answered', 'ответ дан'),
                ],
                default='received',
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'timestamp',
                    models.DateTimeField(auto_now_add=True, null=True),
                ),
                (
                    'from_status',
                    models.CharField(db_column='from', max_length=20),
                ),
                ('to', models.CharField(max_length=100)),
                (
                    'feedback',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='status_logs',
                        to='feedback.feedback',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
