# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0014_auto_20150711_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='billitem',
            name='note',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
