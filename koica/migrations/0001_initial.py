# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(null=True, verbose_name=b'Texte')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('edition_date', models.DateTimeField(null=True, editable=False)),
                ('posted_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-creation_date'],
                'verbose_name': 'R\xe9ponse',
                'verbose_name_plural': 'R\xe9ponse',
            },
        ),
        migrations.CreateModel(
            name='QAComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(null=True, verbose_name=b'Texte')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('answer', models.ForeignKey(related_name='answer_comment', blank=True, to='koica.Answer', null=True)),
                ('posted_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-creation_date'],
                'verbose_name': 'Commentaire',
                'verbose_name_plural': 'Commentaires',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(null=True, verbose_name=b'Texte')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(max_length=25, unique=True, null=True, blank=True)),
                ('title', models.CharField(max_length=120, null=True, verbose_name=b'Titre')),
                ('rating', models.IntegerField(default=0, null=True)),
                ('edition_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('is_duplicated', models.BooleanField(default=False, verbose_name=b'Question dupliqu\xc3\xa9e')),
                ('reported_duplicated_url', models.URLField(null=True, verbose_name=b'Url de la question dupliqu\xc3\xa9e', blank=True)),
                ('duplicated_from', models.ForeignKey(verbose_name=b'Dupliqu\xc3\xa9e depuis', blank=True, to='koica.Question', null=True)),
                ('posted_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('rated_by', models.ManyToManyField(to=settings.AUTH_USER_MODEL, editable=False, blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text=None, verbose_name='Tags')),
            ],
            options={
                'ordering': ['-creation_date'],
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.AddField(
            model_name='qacomment',
            name='question',
            field=models.ForeignKey(related_name='question_comment', blank=True, to='koica.Question', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='question_answer', to='koica.Question', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='rated_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, editable=False, blank=True),
        ),
        migrations.AlterOrderWithRespectTo(
            name='qacomment',
            order_with_respect_to='question',
        ),
        migrations.AlterOrderWithRespectTo(
            name='answer',
            order_with_respect_to='question',
        ),
    ]
