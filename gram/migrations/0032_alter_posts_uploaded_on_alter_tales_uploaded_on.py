# Generated by Django 4.0.1 on 2022-05-07 07:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0031_alter_posts_uploaded_on_alter_tales_uploaded_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 7, 7, 53, 26, 705342, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tales',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 7, 7, 53, 26, 705342, tzinfo=utc)),
        ),
    ]