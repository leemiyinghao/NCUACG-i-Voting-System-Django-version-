# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vote', '0002_auto_20150724_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteticket',
            name='mute',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='votelist',
            name='videoURL',
            field=models.URLField(null=True),
        ),
    ]
