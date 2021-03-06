# Generated by Django 3.1.2 on 2021-01-21 18:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20210121_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='prompts',
            name='prompts_name',
            field=models.CharField(default='None', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 21, 10, 37, 25, 820943)),
        ),
        migrations.AlterField(
            model_name='prompts',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 21, 10, 37, 25, 820943)),
        ),
        migrations.AlterField(
            model_name='song',
            name='added_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 21, 10, 37, 25, 820943)),
        ),
    ]
