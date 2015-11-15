# -*- coding: utf-8 -*-

from datetime import datetime 
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.forms.models import modelform_factory
from django.forms import Textarea, TextInput
from django.contrib import messages
from koica.models import Question, Answer, QAComment
from taggit.models import Tag
from utils import UserCheckMixin, sanitize_html
from django.conf import settings

class QuestionListView(ListView):
    model = Question
    paginate_by = 25
    queryset=Question.objects.all().select_related('posted_by','duplicated_from').prefetch_related('rated_by','question_answer','tags')
    context_object_name='questions'
    
    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['template_to_extend'] = "base.html"
        return context
    

class QuestionCreateView(UserCheckMixin, CreateView):
    model = Question
    form_class =  modelform_factory(Question, 
                                    fields=['title','text','tags'], 
                                    widgets={
                                             "title": TextInput(attrs={'size':'69'}),
                                             "text": Textarea(attrs={'rows':'12','cols':'80'}),
                                             "tags": TextInput(attrs={'size':'40','title':'Liste de mots clés séparés par une virgule. En mettre au moins un correspondant au sujet de votre post'})
                                             }
                                    )
    user_check_failure_path = settings.LOGIN_URL
    
    
    def get_success_url(self):
        return reverse('question-list')
    
    def check_user(self, user):
        if user.is_active:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        context['template_to_extend'] = "base.html"
        context['tags']=Tag.objects.all()
        return context
    
    def form_valid(self, form, **kwargs):   
        obj = form.save(commit=False)
        obj.posted_by = self.request.user
        obj.posted_by_username = self.request.user.username
        obj.save()
        return super(QuestionCreateView, self).form_valid(form)
    

class QuestionDetailView(TemplateView): 
    template_name = 'koica/question_detail.html'
    
    def query_set(self):
        queryset = Question.objects.filter(slug=self.kwargs['slug']).select_related('posted_by','duplicated_from').prefetch_related('rated_by','tags','question_comment','question_answer')[0]
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        question = Question.objects.filter(slug=self.kwargs['slug']).select_related('posted_by','duplicated_from').prefetch_related('question_comment','rated_by','tags')[0]
        answers = Answer.objects.filter(question=question).select_related('posted_by').prefetch_related('answer_comment')
        context['template_to_extend'] = "base.html"
        context['question'] = question
        context['answers'] = answers
        context['koica_base_url'] = getattr(settings, 'KOICA_BASE_URL_SLUG', 'questions')
        return context
    
    
class AnswerCreateView(UserCheckMixin, CreateView):
    model = Answer
    template_name = 'koica/answer_form.html'
    user_check_failure_path = settings.LOGIN_URL
    form_class =  modelform_factory(Answer, 
                                    fields=['text'], 
                                    widgets={
                                             "text": Textarea(attrs={'rows':'12','cols':'80'}),
                                             }
                                    )
    
    def check_user(self, user):
        if user.is_active:
            return True
        return False
    
    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            return reverse('question-list')
        return reverse('question-detail', kwargs={'slug': slug})
    
    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(**kwargs)
        context['question'] = Question.objects.filter(slug=self.kwargs['slug'])[0]
        #~ if bad url or reference
        if not context['question']:
            raise Http404
        context['template_to_extend'] = "base.html"
        return context
        
    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        obj.posted_by = self.request.user
        obj.posted_by_username = self.request.user.username
        context = self.get_context_data(**kwargs)
        obj.question = context['question']
        obj.save()
        return super(AnswerCreateView, self).form_valid(form)
    
    
class CommentCreateView(UserCheckMixin, CreateView):
    model = QAComment
    template_name = 'koica/comment_form.html'
    user_check_failure_path = settings.LOGIN_URL
    form_class =  modelform_factory(QAComment, 
                                    fields=['text'],
                                    widgets={
                                             "text": Textarea(attrs={'rows':'12','cols':'80'}),
                                             }
                                    )
    
    def check_user(self, user):
        if user.is_active:
            return True
        return False
    
    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            return reverse('question-list')
        return reverse('question-detail', kwargs={'slug': slug})
    
    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['question'] = Question.objects.filter(slug=self.kwargs['slug'])[0]
        #~ if bad url or reference
        if not context['question']:
            raise Http404
        context['template_to_extend'] = "base.html"
        return context
        
    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        obj.posted_by = self.request.user
        obj.posted_by_username = self.request.user.username
        context = self.get_context_data(**kwargs)
        obj.question = context['question']
        obj.save()
        return super(CommentCreateView, self).form_valid(form)
    
    
class CommentAnswerCreateView(UserCheckMixin, CreateView):
    model = QAComment
    template_name = 'koica/comment_answer_form.html'
    user_check_failure_path = settings.LOGIN_URL
    form_class =  modelform_factory(QAComment, 
                                    fields=['text'], 
                                    widgets={
                                             "text": Textarea(attrs={'rows':'12','cols':'80'}),
                                             }
                                    )
    
    def check_user(self, user):
        if user.is_active:
            return True
        return False
    
    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            return reverse('question-list')
        return reverse('question-detail', kwargs={'slug': slug})
    
    def get_context_data(self, **kwargs):
        context = super(CommentAnswerCreateView, self).get_context_data(**kwargs)
        qs = Question.objects.filter(slug=self.kwargs['slug']).prefetch_related('question_answer')
        context['question'] = qs[0]
        context['answer'] = qs[0].question_answer.filter(pk=self.kwargs['answer_pk'])[0]
        #~ if bad url or reference
        if not context['question']:
            raise Http404
        context['template_to_extend'] = "base.html"
        return context
        
    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        obj.posted_by = self.request.user
        obj.posted_by_username = self.request.user.username
        context = self.get_context_data(**kwargs)
        obj.answer = context['answer']
        obj.save()
        return super(CommentAnswerCreateView, self).form_valid(form)
    
    
def updateQuestionRatingView(request, slug, operator):
    if not request.user.is_authenticated or not request.user.is_active:
        messages.info(request, 'Vous devez vous logguer pour voter')
        return HttpResponse("")
    if request.is_ajax():
        try:
            operator = request.POST['operator']
            question_slug = request.POST['question_slug']
        except:
            return HttpResponse('Error Response') # incorrect post
        question = Question.objects.filter(slug=question_slug)[0]
        user_can_rate = False
        if request.user == question.posted_by:
            messages.info(request, "On ne vote pas une question qu'on a posée soi-même")
            return HttpResponse("")
        if request.user not in question.rated_by.all():
            user_can_rate = True
        else:
            messages.info(request, 'Vous avez déjà voté pour cette question')
            return HttpResponse("")
        if user_can_rate:
            if operator == 'plus':
                question.rating += 1
            elif operator == 'minus':
                question.rating -= 1
            question.rated_by.add(request.user)
            question.save()
        return HttpResponse("")
    else:
        raise Http404
    
    
class QuestionRatingView(DetailView): 
    model = Question
    context_object_name = 'question'
    template_name = "koica/display_rating.html"
    
    def query_set(self):
        queryset = Question.objects.filter(slug=self.kwargs['slug'])[0]
        return queryset
    
def updateAnswerRatingView(request, pk, operator):
    if not request.user.is_authenticated or not request.user.is_active:
        messages.info(request, 'Vous devez vous logguer pour voter')
        return HttpResponse("")
    if request.is_ajax():
        try:
            operator = request.POST['operator']
            answer_pk = request.POST['answer_pk']
        except:
            return HttpResponse('Error Response') # incorrect post
            messages.info(request, "Erreur - "+str(request.POST))
        answer = Answer.objects.filter(pk=answer_pk)[0]
        user_can_rate = False
        if request.user == answer.posted_by:
            messages.info(request, "On ne vote pas une réponse qu'on a posée soi-même")
            return HttpResponse("")
        if request.user not in answer.rated_by.all():
            user_can_rate = True
        else:
            messages.info(request, 'Vous avez déjà voté pour cette réponse')
            return HttpResponse("")
        if user_can_rate:
            if operator == 'plus':
                answer.rating += 1
            elif operator == 'minus':
                answer.rating -= 1
            answer.rated_by.add(request.user)
            answer.save()
        return HttpResponse("")
    else:
        raise Http404
    
    
class AnswerRatingView(DetailView): 
    model = Answer
    context_object_name = 'answer'
    template_name = "koica/display_answer_rating.html"
    
    def query_set(self):
        queryset = Answer.objects.filter(pk=self.kwargs['pk'])[0]
        return queryset
    
    
def approveAnswerView(request, answer_id):
    if request.is_ajax():
        try:
            answer_id = request.POST['answer_id']
            answer = Answer.objects.filter(pk=answer_id)[0]
        except:
            return HttpResponse("")
        if not answer.question.posted_by == request.user:
            return HttpResponse("")
        else:
            answer.approved = True
            answer.save()
            #messages.info(request, "Réponse validée")
        return HttpResponse("")
    else:
        raise Http404
    
    
class AnswerApprovedView(UserCheckMixin, DetailView): 
    model = Answer
    template_name = "koica/display_approved.html"
    user_check_failure_path = ''
    
    def check_user(self, user):
        answer = self.query_set()
        if answer.question.posted_by == user:
            return True
        return False
    
    def query_set(self):
        queryset = Answer.objects.filter(pk=self.kwargs['pk'])[0]
        return queryset
    
    
class QuestionTagView(ListView):
    template_name = "koica/tag.html"
    context_object_name = "questions"
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Question.objects.all().filter(tags__slug__iexact=self.kwargs['slug'])
        #queryset=Question.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(QuestionTagView,self).get_context_data(**kwargs)
        #~ have to clean the tag slug as it comes from the url and is not safe
        context['tag_slug'] = sanitize_html(self.kwargs['slug'])
        context['template_to_extend'] = "base.html"
        return context  
    
class QuestionEditView(UserCheckMixin, UpdateView):  
    template_name = "koica/update_question_form.html"
    form_class =  modelform_factory(Question, 
                                    fields=['title','text'], 
                                    widgets={
                                             "title": TextInput(attrs={'size':'69'}),
                                             "text": Textarea(attrs={'rows':'12','cols':'80'})
                                             }
                                    )
    user_check_failure_path = settings.LOGIN_URL

    def get_queryset(self):
        queryset = Question.objects.filter(slug=self.kwargs['slug'])
        return queryset
    
    def check_user(self, user):
        question = self.get_queryset()[0]
        if question.posted_by == user:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super(QuestionEditView,self).get_context_data(**kwargs)
        context['template_to_extend'] = "base.html"
        return context
    
    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        obj.posted_by = self.request.user
        obj.posted_by_username = self.request.user.username
        obj.edition_date = datetime.now()
        obj.save()
        return super(QuestionEditView, self).form_valid(form)
 
    
class AnswerEditView(UserCheckMixin, UpdateView):  
    template_name = "koica/update_answer_form.html"
    context_object_name = 'answer'
    form_class =  modelform_factory(Answer, 
                                    fields=['text'], 
                                    widgets={
                                             "text": Textarea(attrs={'rows':'12','cols':'80'})
                                             }
                                    )
    user_check_failure_path = settings.LOGIN_URL
    
    def get_success_url(self):
        return reverse('question-detail', args=(self.get_queryset()[0].question.slug, ))

    def get_queryset(self):
        queryset = Answer.objects.filter(pk=self.kwargs['pk'])
        return queryset
    
    def check_user(self, user):
        answer = self.get_queryset()[0]
        if answer.posted_by == user:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super(AnswerEditView,self).get_context_data(**kwargs)
        context['template_to_extend'] = "base.html"
        return context
    
    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        obj.posted_by = self.request.user
        obj.posted_by_username = self.request.user.username
        obj.edition_date = datetime.now()
        obj.save()
        return super(AnswerEditView, self).form_valid(form)
    
    
class QuestionReportDuplicatedView(UserCheckMixin, UpdateView): 
    template_name = "koica/report_duplicated.html"
    user_check_failure_path = settings.LOGIN_URL
    context_object_name = "question"
    form_class =  modelform_factory(Question, 
                                    fields=['reported_duplicated_url'], 
                                    widgets={
                                             "reported_duplicated_url": TextInput(attrs={'size':'60:'})
                                             }
                                    )
    
    def check_user(self, user):
        if user.is_active:
            return True
        return False
    
    def get_queryset(self):
        queryset = Question.objects.filter(slug=self.kwargs['slug'])
        return queryset
    
    def get_success_url(self):
        return reverse('question-detail', args=(self.get_queryset()[0].slug, ))
    
    def get_context_data(self, **kwargs):
        context = super(QuestionReportDuplicatedView,self).get_context_data(**kwargs)
        context['template_to_extend'] = "base.html"
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        if form.cleaned_data['reported_duplicated_url']:
            commit=False
            if not obj.flaged_as_duplicated:
                obj.flaged_as_duplicated = True
                commit=True
            if not obj.reported_duplicated_url:
                obj.reported_duplicated_url = form.cleaned_data['reported_duplicated_url']
                messages.info(self.request, 'Duplicata signalé, traitement en attente. Merci de votre participation.')
                commit=True
            else:
                messages.info(self.request, "Duplicata déjà signalé en attente de traitement. Merci de votre participation.")
            if commit:
                obj.save()
        else:
            messages.info(self.request, "Merci de fournir l'adresse de la question dupliquée")
        return super(QuestionReportDuplicatedView, self).form_valid(form)
    
    
