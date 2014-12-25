# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0005_auto_20141224_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
