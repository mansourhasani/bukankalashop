# Generated by Django 3.2.14 on 2022-08-28 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tel',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
