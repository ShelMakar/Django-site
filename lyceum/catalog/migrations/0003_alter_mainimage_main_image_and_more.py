# Generated by Django 4.2.16 on 2024-10-23 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_mainimage_options_alter_mainimage_main_image'),
    ]

    operations = [
        migrations.AlterField(
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
        migrations.AlterField(
            model_name='mainimage',
            name='main_images',
            field=models.ImageField(
                help_text='Выберите изображение',
                upload_to='uploads/',
                verbose_name='Будет приведено к размеру 300х300',
            ),
        ),
    ]
