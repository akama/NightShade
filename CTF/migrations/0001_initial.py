# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import CTF.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('points', models.IntegerField()),
                ('key', models.CharField(default=CTF.models.genRandomFlag, max_length=20)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.DateTimeField(auto_now_add=True)),
                ('challenge', models.ForeignKey(to='CTF.Challenge')),
                ('contest', models.ForeignKey(to='CTF.Contest')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='challenge',
            name='contest',
            field=models.ForeignKey(to='CTF.Contest'),
            preserve_default=True,
        ),
    ]
