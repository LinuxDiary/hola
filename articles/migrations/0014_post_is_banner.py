# Generated by Django 2.1 on 2018-12-18 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_category_show_in_nav'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否展示为轮播'),
        ),
    ]
