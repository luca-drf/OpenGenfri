# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0004_auto_20141224_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='priority',
            field=models.PositiveSmallIntegerField(default=3),
            preserve_default=True,
        ),
    ]
