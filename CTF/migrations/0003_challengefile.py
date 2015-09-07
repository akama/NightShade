# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0002_auto_20150907_0641'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'')),
                ('challenge', models.ForeignKey(to='CTF.Challenge')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
