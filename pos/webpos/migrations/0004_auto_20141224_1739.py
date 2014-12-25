# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0003_auto_20141224_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='priority',
            field=models.PositiveSmallIntegerField(default=3),
            preserve_default=True,
        ),
    ]
