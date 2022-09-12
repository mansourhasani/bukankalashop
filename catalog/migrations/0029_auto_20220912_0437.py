# Generated by Django 3.2.14 on 2022-09-12 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0028_auto_20220912_0413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'برند', 'verbose_name_plural': 'برندها'},
        ),
        migrations.AlterModelOptions(
            name='classes',
            options={'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.AlterModelOptions(
            name='package_type',
            options={'verbose_name': 'نوع بسته بندی', 'verbose_name_plural': 'نوع بسته بندی'},
        ),
        migrations.AlterField(
            model_name='brand',
            name='brand_name',
            field=models.CharField(max_length=200, verbose_name='نام برند'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=models.ImageField(upload_to='brand', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='classes',
            name='class_name',
            field=models.CharField(max_length=200, verbose_name='نام دسته بندی'),
        ),
        migrations.AlterField(
            model_name='classes',
            name='sub_clas',
            field=models.BooleanField(default=False, verbose_name=' زیر دسته بندی '),
        ),
        migrations.AlterField(
            model_name='classes',
            name='sub_classes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub', to='catalog.classes', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='package_type',
            name='package_name',
            field=models.CharField(max_length=200, verbose_name='نام بسته بندی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tel',
            field=phone_field.models.PhoneField(blank=True, max_length=31, null=True, verbose_name='شماره تماس'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]