# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdd', '0005_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='zip_code',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
