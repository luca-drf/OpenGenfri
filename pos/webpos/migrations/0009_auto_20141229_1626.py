# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webpos', '0008_bill_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='bill',
            name='server',
            field=models.ForeignKey(default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
