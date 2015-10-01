# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0005_auto_20150907_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_type',
            field=models.CharField(default=b'L', max_length=1, choices=[(b'L', b'Listing'), (b'J', b'Jeopardy')]),
            preserve_default=True,
        ),
    ]
