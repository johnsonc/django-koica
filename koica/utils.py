import re
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, Comment
from django.shortcuts import redirect


class UserCheckMixin(object):
    user_check_failure_path = ''  # can be path, url name or reverse_lazy

    def check_user(self, user):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


def render_unique_slug(classname, slug):
    existing_slug = None
    try:
        existing_slug=classname.objects.get(slug=slug).slug
    except:
        pass
    if existing_slug:
        if '_' in existing_slug:
            slug=slug.split('_')[0]+'_'+str(int(slug.split('_')[1])+1)
        else:
            slug=slug+'_1'
        slug=render_unique_slug(classname, slug)
    return slug

def sanitize_html(value, clear=False, remove_pre=False, base_url=None):
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    if not clear:
        taglist = 'p i strong b ul ol li a h1 h2 h3 br img blockquote div'
        if not remove_pre:
            taglist+=' pre'
        validTags = taglist.split()
        validAttrs = 'href src width height lang class'.split()
        urlAttrs = 'href src'.split() # Attributes which should have a URL
    else:
        validTags = ''
        validAttrs = ''
        urlAttrs = []
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val) # Calculate the absolute url
                tag.attrs.append((attr, val))
    return soup.renderContents().decode('utf8')