# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import CTF.models


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0004_auto_20150907_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengefile',
            name='fileObject',
            field=models.FileField(upload_to=CTF.models.challengeFilePath),
            preserve_default=True,
        ),
    ]
