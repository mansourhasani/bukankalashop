# Generated by Django 3.2.14 on 2022-09-12 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20220910_1731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'کد تخفیف', 'verbose_name_plural': 'کد تخفیف'},
        ),
        migrations.AlterModelOptions(
            name='itemorder',
            options={'verbose_name': 'اقلام سفارش', 'verbose_name_plural': 'اقلام سفارشات'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارشات'},
        ),
    ]
