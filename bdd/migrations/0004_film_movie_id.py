# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdd', '0003_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='movie_id',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
