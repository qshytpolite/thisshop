# Generated by Django 4.2.13 on 2025-02-09 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_alter_banner_desktop_image_alter_banner_mobile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Optional subtitle', max_length=100),
        ),
    ]
