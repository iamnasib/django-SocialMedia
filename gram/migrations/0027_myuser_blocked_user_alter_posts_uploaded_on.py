# Generated by Django 4.0.1 on 2022-04-14 09:42

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0026_alter_posts_uploaded_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='blocked_user',
            field=models.ManyToManyField(blank=True, related_name='blocked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='posts',
            name='uploaded_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 14, 9, 42, 37, 988452, tzinfo=utc)),
        ),
    ]
