# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webpos', '0007_auto_20141224_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 24, 17, 56, 51, 308865, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
