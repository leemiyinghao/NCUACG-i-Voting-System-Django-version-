# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Vote', '0004_auto_20150728_2141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fetchvote',
            options={},
        ),
        migrations.AlterModelOptions(
            name='votelist',
            options={},
        ),
        migrations.AlterModelOptions(
            name='voteticket',
            options={},
        ),
        migrations.AddField(
            model_name='votelist',
            name='hashSetKey',
            field=models.CharField(default=b'7505d64a54e061b7acd5', max_length=50, verbose_name=b'set key'),
        ),
        migrations.AddField(
            model_name='voteticket',
            name='hashUserName',
            field=models.CharField(default=b'7505d64a54e061b7acd5', max_length=20, verbose_name=b'hash id'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='expireDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 3, 9, 30, 31, 445973, tzinfo=utc), verbose_name=b'expire date'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='pubDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 31, 9, 30, 31, 445931, tzinfo=utc), verbose_name=b'publish date'),
        ),
    ]
