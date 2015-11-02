# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0007_challenge_regex_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contest_type',
            field=models.CharField(default=b'L', max_length=1, choices=[(b'L', b'Listing'), (b'J', b'Jeopardy'), (b'B', b'Blind')]),
            preserve_default=True,
        ),
    ]
