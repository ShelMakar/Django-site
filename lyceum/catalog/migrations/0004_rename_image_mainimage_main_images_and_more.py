# Generated by Django 4.2.16 on 2024-10-23 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_mainimage_item_images_item_main_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainimage',
            old_name='image',
            new_name='main_images',
        ),
        migrations.RemoveField(
            model_name='item',
            name='images',
        ),
        migrations.RemoveField(
            model_name='item',
            name='main_image',
        ),
        migrations.AddField(
            model_name='mainimage',
            name='main_image',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mainimage',
                to='catalog.item',
                verbose_name='главное изображение',
            ),
        ),
        migrations.CreateModel(
            name='SecondImages',
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
                    'image',
                    models.ImageField(
                        upload_to='uploads/', verbose_name='изображение'
                    ),
                ),
                (
                    'images',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='catalog.item',
                        verbose_name='изображения',
                    ),
                ),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
            },
        ),
    ]
