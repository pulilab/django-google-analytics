from .models import Analytics
from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin, Site

class AnalyticsInlineAdmin(admin.StackedInline):
    model = Analytics

class AnalyticsSiteAdmin(SiteAdmin):
    inlines = [AnalyticsInlineAdmin]

admin.site.unregister(Site)
admin.site.register(Site, AnalyticsSiteAdmin)