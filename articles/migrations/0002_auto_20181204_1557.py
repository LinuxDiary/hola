# Generated by Django 2.1 on 2018-12-04 15:57

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': '所有文章', 'verbose_name_plural': '所有文章'},
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=mdeditor.fields.MDTextField(),
        ),
    ]
