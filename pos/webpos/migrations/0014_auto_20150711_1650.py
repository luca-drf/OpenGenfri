# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0013_auto_20150707_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='printable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='customer_id',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='deleted_by',
            field=models.CharField(max_length=40, blank=True),
        ),
    ]
