# Generated by Django 3.2.14 on 2022-08-18 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_users_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='image',
            field=models.ImageField(upload_to='product'),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='number_in_the_box',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='price',
            field=models.PositiveIntegerField(help_text='قیمت اصلی را وارد کنید'),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='reduc_price',
            field=models.PositiveIntegerField(help_text='قیمت  با تخفیف را وارد کنید'),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='weight',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='cost',
            field=models.PositiveIntegerField(),
        ),
    ]
