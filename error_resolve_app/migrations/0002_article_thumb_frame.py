# Generated by Django 3.1.5 on 2021-02-20 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error_resolve_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumb_frame',
            field=models.IntegerField(default=0),
        ),
    ]
