# Generated by Django 2.1.5 on 2019-01-21 12:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190121_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 21, 12, 49, 13, 127929, tzinfo=utc)),
        ),
    ]
