# Generated by Django 4.0.1 on 2022-04-05 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0020_rename_is_deleted_myuser_is_deactivated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 5, 12, 39, 14, 866256)),
        ),
    ]