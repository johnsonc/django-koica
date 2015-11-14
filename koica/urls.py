from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from koica.views import QuestionListView, QuestionCreateView, QuestionDetailView, AnswerCreateView, CommentCreateView, CommentAnswerCreateView, updateQuestionRatingView, QuestionRatingView, AnswerRatingView, updateAnswerRatingView, approveAnswerView, AnswerApprovedView, QuestionTagView, QuestionEditView, AnswerEditView, QuestionReportDuplicatedView

urlpatterns = [
    url(r'^tag/(?P<slug>[-_\w]+)/$', QuestionTagView.as_view(), name='question-tag'),
    url(r'^$', QuestionListView.as_view(), name='question-list'),
    url(r'^add/$', login_required(QuestionCreateView.as_view()), name="question-add"),
    url(r'^repondre/(?P<slug>[-_\w]+)/$', login_required(AnswerCreateView.as_view()), name='answer-form'),
    url(r'^editer/(?P<slug>[-_\w]+)/$', login_required(QuestionEditView.as_view()), name='edit-form'),
    url(r'^reponse/editer/(?P<pk>[0-9]+)/$', login_required(AnswerEditView.as_view()), name='answer-edit-form'),
    url(r'^commenter/(?P<slug>[-_\w]+)/(?P<answer_pk>\d+)/$', login_required(CommentAnswerCreateView.as_view()), name='comment-answer-form'),
    url(r'^commenter/(?P<slug>[-_\w]+)/$', login_required(CommentCreateView.as_view()), name='comment-form'),
    url(r'^(?P<slug>[-_\w]+)/rating/$', QuestionRatingView.as_view(), name='question-rating-view'),
    url(r'^answer/(?P<pk>[0-9]+)/rating/$', AnswerRatingView.as_view(), name='answer-rating'),
    url(r'^(?P<slug>[-_\w]+)/rating/(?P<operator>[\w]+)/$', updateQuestionRatingView, name='question-rating-rate'),
    url(r'^answer/(?P<pk>[0-9]+)/rating/(?P<operator>[\w]+)/$', updateAnswerRatingView, name='anwser-rating-rate'),
    url(r'^(?P<answer_id>[0-9]+)/approve/$', login_required(approveAnswerView), name='approve-answer'),
    url(r'^(?P<pk>[0-9]+)/approved/$', login_required(AnswerApprovedView.as_view()), name='answer-approved'),
    url(r'^(?P<slug>[-_\w]+)/duplicat/signaler/$', QuestionReportDuplicatedView.as_view(), name='question-report-duplicated'),
    url(r'^(?P<slug>[-_\w]+)/$', QuestionDetailView.as_view(), name='question-detail'),
]