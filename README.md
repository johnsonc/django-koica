Django Koica
==============

Simple Q&amp;A application with bootstrap templates [ warning: this app is only available for french language at the time]

Dependencies
--------------

- django-pygments
- jquery
- jquery ui
- bootstrap

Install
--------------

- Clone the repository
- Get the dependencies
- Add 'koica', and 'django_pygments', to INSTALLED_APPS
- Add this to urls.py:

		from django.conf import settings
		
		koica_base_url = getattr(settings, 'KOICA_BASE_URL_SLUG', 'questions')

		urlpatterns = patterns('',
		#...
		url(r'^'+koica_base_url+'/', include('koica.urls')),
	    )
    
- Collect static files
- Run migrations
- In your base template ("base.html") these blocks are required:

		{% block extra_header %}{% endblock %} in <head>
		{% block title %}{% endblock %} in <head><title>
		<div id="content" class="container">{% block content %}{% endblock %}</div> in <body>

Options
--------------

To choose an url for your app add this setting (if not set default is '/questions/'):

	KOICA_BASE_URL_SLUG = 'forum'

Note: this application is compatible with [django-xadmin](https://github.com/sshwsfc/django-xadmin)

Todo
--------------

- [ ] Translate in english (not internationalized yet)
- [ ] Options to embed js and css dependencies
- [ ] Tests
- [ ] Make a release and package it in pip
