# Generated by Django 4.0.1 on 2022-04-12 06:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0025_alter_posts_uploaded_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 12, 6, 35, 43, 290684, tzinfo=utc)),
        ),
    ]