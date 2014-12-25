# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0006_auto_20141224_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='total',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='billitem',
            name='total',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
    ]
