from django.core.urlresolvers import reverse
from django.test import Client
from django.conf import settings
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from koica.models import Question, Answer
from koica.views import QuestionDetailView

KOICA_BASE_URL_SLUG = getattr(settings, 'KOICA_BASE_URL_SLUG','questions')


class QuestionModelsTest(TestCase):
    
    def create_question(self, slug="question_s", text="Test Question text", title="Test Question Title"):
        return Question.objects.create(slug=slug, text=text, title=title)
    
    def test_question_creation(self):
        question=self.create_question()
        self.assertTrue(isinstance(question, Question))
        self.assertEqual(question.__unicode__(), question.title+' - '+str(question.pk))
        self.assertEqual(question.get_absolute_url(), '/'+KOICA_BASE_URL_SLUG+'/'+question.slug+'/')
        self.assertEqual(question.title, "Test Question Title")
        self.assertEqual(question.text, "Test Question text")
        
    def test_blank_slug(self):
        question=self.create_question(slug="", title='Test title')
        self.assertEqual(question.slug, "test-title")
        
    def test_unique_slug(self):
        question1=self.create_question(slug="", title='Test title')
        question2=self.create_question(slug="", title='Test title')
        self.assertNotEqual(question1.slug, question2.slug)
        
    def test_html_sanitization(self):
        question=self.create_question(title="<iframe>Test Question Title</iframe>")
        self.assertEqual(question.title, "Test Question Title")
        
    def test_html_sanitization_escapejs(self):
        question=self.create_question(text="<a href=\"javascript:alert('blop')\">Test</a> Question <i>text</i>")
        self.assertEqual(question.text, "<a href=\"alert('blop')\">Test</a> Question <i>text</i>")
   
        
class QuestionViewsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        
    def create_question(self, slug="question_s", text="Test Question text", title="Test Question Title"):
        return Question.objects.create(slug=slug, text=text, title=title)
    
    def create_question_and_answer(self, question_slug="question_s", text="Test Answer text"):
        question=self.create_question(slug=question_slug)
        answer=Answer.objects.create(question=question, text=text)
        return (question, answer)

    def test_questions_list(self):
        # Issue a GET request.
        response = self.client.get('/'+KOICA_BASE_URL_SLUG+'/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        #~ Check if the right view is served
        from koica.views import QuestionListView
        self.assertEqual(response.resolver_match.func.__name__, QuestionListView.as_view().__name__)
        
    def test_question_creation_logged_in_user(self):
        request = self.factory.get('/'+KOICA_BASE_URL_SLUG+'/')
        request.user = User.objects.create_user(username='joe', email='joe@mail.com', password='top_secret')
        from koica.views import QuestionCreateView
        response = QuestionCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
    def test_question_creation_anonymous_user(self):
        self.client.logout()
        request = self.factory.get('/'+KOICA_BASE_URL_SLUG+'/')
        request.user = AnonymousUser()
        response = self.client.get(reverse('question-add'))
        self.assertRedirects(response, settings.LOGIN_URL+'?next=/'+KOICA_BASE_URL_SLUG+'/add/')
        
    def test_question_creation_postcontrols(self):
        request = self.factory.get('/'+KOICA_BASE_URL_SLUG+'/')
        request.user = User.objects.create_user(username='bob', email='bob@mail.com', password='top_secret')
        self.client.login(username='bob', password='top_secret')
        response = self.client.post(reverse('question-add'), {
            'title': u'Test title',
            'text': u'Test text',
            'tags':u'hello',
        }, follow=True)
        last_question = Question.objects.latest(field_name='creation_date')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(last_question.title,'Test title')
        self.assertEqual(last_question.text,'Test text')
        #self.assertEqual(last_question.tags,'hello')
        self.assertEqual(last_question.posted_by, request.user)
        self.assertEqual(last_question.posted_by_username, request.user.username)
        
    def test_questions_detail_view(self):
        question, answer=self.create_question_and_answer(question_slug='my_question')
        response = self.client.get(reverse('question-detail',kwargs= {'slug':'my_question'}))
        self.assertEqual(response.status_code, 200)
        #~ Check if the right view is served
        from koica.views import QuestionDetailView
        self.assertEqual(response.resolver_match.func.__name__, QuestionDetailView.as_view().__name__)
        self.assertEqual(question.slug,'my_question')
        #~ check context data
        self.assertEqual(response.context['question'], question)
        answers=Answer.objects.filter(question=question)
        self.assertEqual(len(response.context['answers']), len(answers))
        self.assertEqual(response.context['answers'][0], answer)
        self.assertEqual(response.context['koica_base_url'], KOICA_BASE_URL_SLUG)
        



        
        
        
        
        