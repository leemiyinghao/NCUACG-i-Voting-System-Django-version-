# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FetchVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(max_length=50)),
                ('fetchDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='VoteableUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(max_length=50)),
                ('nickName', models.CharField(max_length=50)),
                ('icon', models.ImageField(default=b'static/usericon/default.png', upload_to=b'usericon')),
            ],
        ),
        migrations.CreateModel(
            name='VoteList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('describe', models.TextField(max_length=500)),
                ('voteType', models.CharField(max_length=1, choices=[(b'v', b'videoVote'), (b's', b'select')])),
                ('pubDate', models.DateTimeField(verbose_name=b'date published')),
                ('expireDate', models.DateTimeField(verbose_name=b'date expire')),
                ('videoURL', models.URLField()),
                ('maxSelectCount', models.IntegerField(default=1)),
                ('videoLength', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VoteTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(max_length=50)),
                ('score', models.IntegerField(default=0)),
                ('doneVideo', models.BooleanField(default=False)),
                ('optionID', models.ForeignKey(to='Vote.Options')),
                ('roomID', models.ForeignKey(to='Vote.VoteList')),
            ],
        ),
        migrations.AddField(
            model_name='options',
            name='roomID',
            field=models.ForeignKey(to='Vote.VoteList'),
        ),
        migrations.AddField(
            model_name='fetchvote',
            name='roomID',
            field=models.ForeignKey(to='Vote.VoteList'),
        ),
    ]
