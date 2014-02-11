from django import template
from django.conf import settings
from ..models import Analytics
from django.contrib.sites.models import Site

from django.template import Context, loader


register = template.Library()

def do_get_analytics(parser, token):
    contents = token.split_contents()
    tag_name = contents[0]
    template_name = 'google_analytics/%s_template.html' % tag_name
    if len(contents) == 2:
        # split_contents() knows not to split quoted strings.
        code = contents[1]
    elif len(contents) == 1:
        code = None
    else:
        raise template.TemplateSyntaxError, "%r cannot take more than one argument" % tag_name
   
    if not code:
        current_site = Site.objects.get_current()
    else:
        if not (code[0] == code[-1] and code[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
        code = code[1:-1]
        current_site = None

    return AnalyticsNode(current_site, code, template_name)
    
class AnalyticsNode(template.Node):
    def __init__(self, site=None, code=None, template_name='google_analytics/analytics_template.html'):
        self.site = site
        self.code = code
        self.template_name = template_name
        
    def render(self, context):
        content = ''
        if self.site:
            try:
                code = self.site.analytics
            except Analytics.DoesNotExist:
                return ''
            else:
                return ''
        elif self.code:
            code = type('Code', (object,), {
                'analytics_code': self.code,
                'analytics_domain': '',
                'track_page_load': False
            })()
        else:
            return ''
        
        if code.analytics_code.strip() != '':
            t = loader.get_template(self.template_name)
            c = Context({
                'analytics_code': code.analytics_code,
                'analytics_domain': code.analytics_domain,
                'track_page_load_time': code.track_page_load,
            })
            return t.render(c)
        else:
            return ''
        
register.tag('analytics', do_get_analytics)
register.tag('analytics_async', do_get_analytics)
