# Generated by Django 4.0.1 on 2022-04-19 07:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0029_alter_posts_uploaded_on_alter_tales_uploaded_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 19, 7, 21, 24, 665363, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tales',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 19, 7, 21, 24, 680988, tzinfo=utc)),
        ),
    ]
