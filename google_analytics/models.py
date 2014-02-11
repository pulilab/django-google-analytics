from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site

class Analytics(models.Model):
    site = models.OneToOneField(Site)
    analytics_code = models.CharField(blank=True, max_length=100)
    analytics_domain = models.CharField(blank=True, max_length=100,
        help_text="You can set here the analytics domain to merge reports with other sites")
    track_page_load = models.BooleanField("Track page load time",
        blank=True, default=False)

    def __unicode__(self):
        return u"%s" % (self.analytics_code)
    
    class Meta:
        verbose_name_plural = "Analytics"
