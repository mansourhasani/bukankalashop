# Generated by Django 3.2.14 on 2022-09-02 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20220902_0456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='image',
        ),
    ]
