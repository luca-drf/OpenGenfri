# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0009_auto_20141229_1626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billitem',
            old_name='total',
            new_name='item_price',
        ),
    ]
