# Generated by Django 3.1.5 on 2021-02-20 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('error_resolve_app', '0004_auto_20210220_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
        migrations.RemoveField(
            model_name='article',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
    ]
