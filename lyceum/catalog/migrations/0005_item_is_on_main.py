# Generated by Django 4.2.16 on 2024-10-28 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_item_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_on_main',
            field=models.BooleanField(
                default=False, verbose_name='на главной'
            ),
        ),
    ]
