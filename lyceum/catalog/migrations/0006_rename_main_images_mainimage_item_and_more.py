# Generated by Django 4.2.16 on 2024-10-29 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_item_is_on_main'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainimage',
            old_name='main_images',
            new_name='item',
        ),
        migrations.RemoveField(
            model_name='mainimage',
            name='main_image',
        ),
        migrations.AddField(
            model_name='mainimage',
            name='image',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='main_image',
                to='catalog.item',
                verbose_name='главное изображение',
            ),
        ),
    ]
