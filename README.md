Django Koica
==============

Simple Q&amp;A application with bootstrap templates

Dependencies
--------------

- django-pygments
- jquery
- jquery ui
- bootstrap

Install
--------------

- Clone the repository
- Add 'koica', and 'django_pygments', to INSTALLLED_APPS
- Add this to urls.py:

		from django.conf import settings
		
		koica_base_url = getattr(settings, 'KOICA_BASE_URL_SLUG', 'questions')

		urlpatterns = patterns('',
		#...
		url(r'^'+koica_base_url+'/', include('koica.urls')),
	    )
    
- Collect static files
- Run migrations

Options
--------------

To choose an url for your app add the settting:

	KOICA_BASE_URL_SLUG = 'forum'


Todo
--------------

- [ ] Tests
- [ ] Package the whole thing in pip
