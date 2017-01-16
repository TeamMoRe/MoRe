# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdd', '0006_auto_20170105_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='movie_id',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='movie_id',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.AddField(
            model_name='rating',
            name='movie',
            field=models.ForeignKey(to='bdd.Film', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(to='bdd.User', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(),
        ),
    ]
