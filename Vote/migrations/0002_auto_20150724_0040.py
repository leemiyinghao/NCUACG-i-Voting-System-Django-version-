# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteableuser',
            name='icon',
            field=models.ImageField(default=b'/static/usericon/default.png', upload_to=b'usericon'),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='voteType',
            field=models.CharField(max_length=1, choices=[(b'v', b'videoVote'), (b's', b'selectVote')]),
        ),
        migrations.AlterField(
            model_name='voteticket',
            name='optionID',
            field=models.ForeignKey(to='Vote.Options', null=True),
        ),
    ]
