# Generated by Django 3.1.5 on 2021-02-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error_resolve_app', '0002_article_thumb_frame'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='upload_file_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
