# Generated by Django 4.2.16 on 2024-10-13 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='is_published',
        ),
    ]
