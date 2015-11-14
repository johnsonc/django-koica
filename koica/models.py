# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from utils import sanitize_html, render_unique_slug


class Contribution(models.Model):
	posted_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
	posted_by_username = models.CharField(max_length=120, null=True, editable=False)
	text = models.TextField(null=True, verbose_name="Texte")
	creation_date = models.DateTimeField(null=True, auto_now_add=True, editable=False)
	
	class Meta:
		abstract = True
	

class Question(Contribution):
	slug = models.SlugField(max_length=25, unique=True, null=True, blank=True)
	title=models.CharField(max_length=120, null=True, blank=False, verbose_name="Titre")
	rating = models.IntegerField(default=0, null=True)
	rated_by = models.ManyToManyField(User, blank=True, editable=False)
	edition_date = models.DateTimeField(null=True, blank=True, editable=False)
	is_duplicated = models.BooleanField(default=False, verbose_name="Question dupliquée")
	duplicated_from = models.ForeignKey('self', null=True, blank=True, verbose_name="Dupliquée depuis")
	flaged_as_duplicated = models.BooleanField(default=False, verbose_name="Question signalée comme dupliquée")
	reported_duplicated_url = models.URLField(null=True, blank=True, verbose_name="Adresse de la question dupliquée")
	tags = TaggableManager(help_text=None)
	
	class Meta:
		verbose_name = 'Question'
		verbose_name_plural = 'Questions'
		ordering = ['-creation_date']
		
	def __unicode__(self):
		return u'%s' % (self.title)+' - '+str(self.pk)
	
	def save(self, *args, **kwargs):
		self.title = sanitize_html(self.title)
		if not self.slug:
			#~ must be unique
			self.slug =render_unique_slug(self.__class__, slugify(self.title))
		self.text = sanitize_html(self.text)	
		super(Question, self).save()
	
	def get_absolute_url(self):
		return reverse('question-detail', args=(self.slug, ))
	
	
class Answer(Contribution):
	question = models.ForeignKey(Question, null=True, related_name="question_answer")	
	rating = models.IntegerField(default=0)
	rated_by = models.ManyToManyField(User, blank=True, editable=False)
	approved = models.BooleanField(default=False)
	edition_date = models.DateTimeField(null=True, editable=False)
	
	
	class Meta:
		ordering = ['-creation_date']
		order_with_respect_to = 'question'
		verbose_name = u'Réponse'
		verbose_name_plural = u'Réponses'
		
		
	def __unicode__(self):
		if settings.DEBUG:
			return u'%s' % (self.question.title)+' - '+str(self.pk)
		else:
			return 'Réponse '+str(self.pk)
		
	def save(self, *args, **kwargs):
		self.text = sanitize_html(self.text)
		super(Answer, self).save()

	
class QAComment(Contribution):
	answer = models.ForeignKey(Answer, null=True, blank=True, related_name="answer_comment")
	question = models.ForeignKey(Question, null=True, blank=True, related_name="question_comment")
	
	class Meta:
		ordering = ['-creation_date']
		order_with_respect_to = 'question'
		verbose_name = u'Commentaire'
		verbose_name_plural = u'Commentaires'
		
	def save(self, *args, **kwargs):
		self.text = sanitize_html(self.text, clear=True)
		super(QAComment, self).save()

	
	
	