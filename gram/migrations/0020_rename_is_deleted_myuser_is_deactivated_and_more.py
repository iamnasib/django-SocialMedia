# Generated by Django 4.0.1 on 2022-03-28 10:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0019_alter_posts_uploaded_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='is_deleted',
            new_name='is_deactivated',
        ),
        migrations.AlterField(
            model_name='posts',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 16, 2, 27, 589040)),
        ),
    ]