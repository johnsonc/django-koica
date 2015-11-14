# -*- coding: utf-8 -*-

import xadmin
from django.utils.text import slugify
from django.conf import settings
from koica.models import Question, QAComment, Answer


class QuestionXadmin(object):
    if 'reversion' in settings.INSTALLED_APPS:
        reversion_enable = True
    show_bookmarks = False
    list_filter = ['flaged_as_duplicated']
    
    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        obj.posted_by_username = request.user.username
        #~ autoslug: necessary when a user posts from the site
        if not obj.slug:
            obj.slug=slugify(obj.title)[-25:]
        obj.save()
    

class AnswerXadmin(object):
    if 'reversion' in settings.INSTALLED_APPS:
        reversion_enable = True
    show_bookmarks = False
    
    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        obj.posted_by_username = request.user.username
        obj.save()


class QACommentXadmin(object):
    if 'reversion' in settings.INSTALLED_APPS:
        reversion_enable = True
    show_bookmarks = False
    #relfield_style = 'fk-ajax'
    
    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        obj.posted_by_username = request.user.username
        obj.save()


xadmin.site.register(Question, QuestionXadmin)
xadmin.site.register(Answer, AnswerXadmin)
xadmin.site.register(QAComment, QACommentXadmin)
