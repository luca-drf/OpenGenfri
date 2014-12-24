# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0002_auto_20141224_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
