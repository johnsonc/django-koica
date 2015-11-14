# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('koica', '0002_auto_20151114_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='reported_duplicated_url',
            field=models.URLField(null=True, verbose_name=b'Adresse de la question dupliqu\xc3\xa9e', blank=True),
        ),
    ]
