# Generated by Django 3.2.14 on 2022-09-01 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_brand_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
    ]