# Generated by Django 4.2.13 on 2025-02-09 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_alter_productvariation_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductVariation',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
