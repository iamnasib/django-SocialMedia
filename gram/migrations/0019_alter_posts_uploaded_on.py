# Generated by Django 4.0.1 on 2022-03-28 08:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0018_alter_posts_uploaded_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 14, 24, 40, 578497)),
        ),
    ]
