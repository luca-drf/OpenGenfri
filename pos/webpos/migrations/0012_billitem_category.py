# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0011_auto_20150706_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='billitem',
            name='category',
            field=models.ForeignKey(to='webpos.Category', null=True),
        ),
    ]
