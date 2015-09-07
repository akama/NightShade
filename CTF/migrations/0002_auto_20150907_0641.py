# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import CTF.models


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='key',
            field=models.CharField(default=CTF.models.genRandomFlag, max_length=200),
            preserve_default=True,
        ),
    ]
