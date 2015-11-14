# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('koica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='posted_by_username',
            field=models.CharField(max_length=120, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='qacomment',
            name='posted_by_username',
            field=models.CharField(max_length=120, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='question',
            name='posted_by_username',
            field=models.CharField(max_length=120, null=True, editable=False),
        ),
    ]
