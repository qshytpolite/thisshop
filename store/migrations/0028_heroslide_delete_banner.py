# Generated by Django 4.2.13 on 2025-02-19 19:38

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='hero_images/')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=200)),
                ('button_text', models.CharField(blank=True, max_length=50, null=True)),
                ('button_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
    ]
