# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NormalVote', '0002_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_describe',
            field=models.TextField(max_length=500),
            preserve_default=True,
        ),
    ]
