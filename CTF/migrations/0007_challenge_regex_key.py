# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0006_contest_contest_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='regex_key',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
