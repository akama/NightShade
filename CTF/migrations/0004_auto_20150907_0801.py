# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0003_challengefile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challengefile',
            old_name='file',
            new_name='fileObject',
        ),
    ]
