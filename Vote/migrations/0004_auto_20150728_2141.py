# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Vote', '0003_auto_20150726_2356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fetchvote',
            options={'verbose_name': 'fetch vote record', 'verbose_name_plural': 'fetch vote records', 'permissions': (('CAN_VIEW_FETCH_VOTE', 'Can view fetch vote record'),)},
        ),
        migrations.AlterModelOptions(
            name='voteableuser',
            options={'verbose_name': 'voteable user', 'verbose_name_plural': 'voteable user list'},
        ),
        migrations.AlterModelOptions(
            name='votelist',
            options={'verbose_name': 'vote', 'verbose_name_plural': 'vote list'},
        ),
        migrations.AlterModelOptions(
            name='voteticket',
            options={'verbose_name': 'vote record', 'verbose_name_plural': 'vote records', 'permissions': (('CAN_VIEW_VOTE_TICKET', 'Can view vote record'),)},
        ),
        migrations.AlterField(
            model_name='fetchvote',
            name='fetchDate',
            field=models.DateTimeField(verbose_name=b'fetch datetime'),
        ),
        migrations.AlterField(
            model_name='fetchvote',
            name='userName',
            field=models.CharField(max_length=50, verbose_name=b'user name'),
        ),
        migrations.AlterField(
            model_name='options',
            name='text',
            field=models.CharField(max_length=500, verbose_name=b'option title'),
        ),
        migrations.AlterField(
            model_name='voteableuser',
            name='icon',
            field=models.ImageField(default=b'/static/usericon/default.png', upload_to=b'usericon', verbose_name=b'user icon'),
        ),
        migrations.AlterField(
            model_name='voteableuser',
            name='nickName',
            field=models.CharField(max_length=50, verbose_name=b'nick name'),
        ),
        migrations.AlterField(
            model_name='voteableuser',
            name='userName',
            field=models.CharField(max_length=50, verbose_name=b'user name'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='describe',
            field=models.TextField(max_length=500, verbose_name=b'vote describe'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='expireDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 31, 13, 41, 58, 726714, tzinfo=utc), verbose_name=b'expire date'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='maxSelectCount',
            field=models.IntegerField(default=1, verbose_name=b'max selection'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='pubDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 28, 13, 41, 58, 726675, tzinfo=utc), verbose_name=b'publish date'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='title',
            field=models.CharField(max_length=50, verbose_name=b'vote title'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='videoLength',
            field=models.IntegerField(default=0, verbose_name=b'video length'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='videoURL',
            field=models.URLField(null=True, verbose_name=b'video URL'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='voteType',
            field=models.CharField(max_length=1, verbose_name=b'vote type', choices=[(b'v', b'videoVote'), (b's', b'selectVote')]),
        ),
        migrations.AlterField(
            model_name='voteticket',
            name='doneVideo',
            field=models.BooleanField(default=False, verbose_name=b'has user done the video?'),
        ),
        migrations.AlterField(
            model_name='voteticket',
            name='mute',
            field=models.BooleanField(default=False, verbose_name=b'mute'),
        ),
        migrations.AlterField(
            model_name='voteticket',
            name='userName',
            field=models.CharField(max_length=50, verbose_name=b'user name'),
        ),
    ]
