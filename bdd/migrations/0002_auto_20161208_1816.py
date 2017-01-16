# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdd', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='auteur',
        ),
        migrations.RemoveField(
            model_name='film',
            name='contenu',
        ),
        migrations.RemoveField(
            model_name='film',
            name='date',
        ),
        migrations.RemoveField(
            model_name='film',
            name='titre',
        ),
        migrations.AddField(
            model_name='film',
            name='imdb_url',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='film',
            name='release_date',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='film',
            name='title',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='film',
            name='video_release_date',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
