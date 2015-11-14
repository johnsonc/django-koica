# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('koica', '0003_auto_20151114_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-creation_date'], 'verbose_name': 'R\xe9ponse', 'verbose_name_plural': 'R\xe9ponses'},
        ),
        migrations.AddField(
            model_name='question',
            name='flaged_as_duplicated',
            field=models.BooleanField(default=False, verbose_name=b'Question signal\xc3\xa9e comme dupliqu\xc3\xa9e'),
        ),
    ]
