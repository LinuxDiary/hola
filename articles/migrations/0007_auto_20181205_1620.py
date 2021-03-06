# Generated by Django 2.1 on 2018-12-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20181205_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='short_name',
            field=models.CharField(default='', max_length=30, verbose_name='自定义链接'),
        ),
        migrations.AlterField(
            model_name='post',
            name='baidu_download',
            field=models.URLField(blank=True, null=True, verbose_name='百度网盘下载地址'),
        ),
        migrations.AlterField(
            model_name='post',
            name='short_title',
            field=models.CharField(max_length=100, verbose_name='自定义链接'),
        ),
    ]
