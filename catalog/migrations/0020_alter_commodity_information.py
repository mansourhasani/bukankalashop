# Generated by Django 3.2.14 on 2022-09-03 15:27

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_alter_commodity_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='information',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]