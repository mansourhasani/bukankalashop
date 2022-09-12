# Generated by Django 3.2.14 on 2022-09-01 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_remove_commodity_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
    ]
