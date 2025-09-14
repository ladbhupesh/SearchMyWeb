from django.core.management.base import BaseCommand
from django.utils import timezone
from UserManagementApp.crawl_website import *

class Command(BaseCommand):
    help = 'Start Crawlers'

    def handle(self, *args, **kwargs):
        #index_website_scheduler()
        crawl_website_scheduler()
