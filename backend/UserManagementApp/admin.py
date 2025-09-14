from django.contrib import admin
from UserManagementApp.models import *
# Register your models here.

admin.site.register(User)

class WebsiteLinkAdmin(admin.ModelAdmin):
    list_display = ('link', 'index_level', 'last_indexed', 'is_indexed', 'is_crawl',)

admin.site.register(WebsiteLink, WebsiteLinkAdmin)

admin.site.register(SearchQueryLog)

admin.site.register(WebsiteLinkClick)

admin.site.register(DailyAnalyticsReports)

admin.site.register(DailyWorldCluodAnalytics)

admin.site.register(StateWiseTrafficAnalytic)