# Generated by Django 3.1 on 2021-02-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_postimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]