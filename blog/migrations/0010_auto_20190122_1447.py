# Generated by Django 2.1.5 on 2019-01-22 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190122_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, default='', null=True),
        ),
    ]
