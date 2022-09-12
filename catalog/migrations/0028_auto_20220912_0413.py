# Generated by Django 3.2.14 on 2022-09-11 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_commodity_favourite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Managers',
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات'},
        ),
        migrations.AlterModelOptions(
            name='commodity',
            options={'ordering': ['brand'], 'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AlterModelOptions(
            name='images',
            options={'verbose_name': 'تصویر', 'verbose_name_plural': 'تصاویر'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'پروفایل', 'verbose_name_plural': 'پروفایل ها'},
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
