# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('customer_id', models.CharField(max_length=20)),
                ('customer_name', models.CharField(max_length=40)),
                ('total', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('total', models.IntegerField()),
                ('bill', models.ForeignKey(to='webpos.Bill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('priority', models.PositiveSmallIntegerField()),
                ('enabled', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('priority', models.PositiveSmallIntegerField()),
                ('enabled', models.BooleanField(default=False)),
                ('price', models.IntegerField()),
                ('category', models.ForeignKey(to='webpos.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=30)),
                ('enabled', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='billitem',
            name='item',
            field=models.ForeignKey(to='webpos.Item'),
            preserve_default=True,
        ),
    ]
