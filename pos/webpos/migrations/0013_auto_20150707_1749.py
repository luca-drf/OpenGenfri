# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0012_billitem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='deleted_by',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='server',
            field=models.CharField(max_length=40),
        ),
    ]
