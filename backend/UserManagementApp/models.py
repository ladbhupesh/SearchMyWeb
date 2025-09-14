from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from UserManagementApp.constants import USER_CHOICES
from UserManagementApp.utils import logger, logger_extra, HTTP_CHOICES
from django.utils import timezone
import uuid
from django.db.models import Avg, Q, Sum, Count
# Create your models here.

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    role = models.CharField(max_length=256,
                            null=False,
                            blank=False,
                            choices=USER_CHOICES)

class AuthToken(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    last_used_at = models.DateTimeField(default=timezone.now)

class WebsiteLink(models.Model):

    link = models.CharField(max_length=600,
                            null=True,
                            blank=True,
                            help_text="Website link which will be crawled and indexed.", db_index = True)

    click_count = models.IntegerField(
        default=0, help_text="Number of times users clicked on the link.")

    search_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index = True, help_text="Selected user will see the crawled links in EasyChat console and can do searching.")

    index_level = models.IntegerField(null=True, blank=True,
                                      help_text='Indexing will be done till the given depth. Use "-1" for indexing the whole website.')

    hyper_text = models.CharField(max_length=5,
                                  null=True,
                                  blank=True,
                                  choices=HTTP_CHOICES,
                                  help_text="Website with the chooseen hyper text will be crawled")

    last_indexed = models.DateTimeField(
        default=timezone.now, null=True, blank=True, help_text="Date and time when the website is indexed.")

    is_indexed = models.BooleanField(
        default=False, help_text="Designates that website link is indexed in elasticsearch or not.")

    is_crawl = models.BooleanField(
        default=False, help_text="Designates that it should be crawled or not.")

    created_date = models.DateTimeField(default=timezone.now, db_index = True)

    def __str__(self):
        try:
            return self.link
        except Exception:
            return "Empty links"

    def save(self, *args, **kwargs):
        super(WebsiteLink, self).save(*args, **kwargs)
        logger.info("WebsiteLink has been save successfully", extra=logger_extra)

    class Meta:
        verbose_name = 'WebsiteLink'
        verbose_name_plural = 'WebsiteLinks'
        unique_together = (('link', 'search_user'),)

class SearchQueryLog(models.Model):
    query = models.TextField()

    result = models.TextField()

    search_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index = True, help_text="Selected user will see the crawled links in EasyChat console and can do searching.")    

    created_time = models.DateTimeField(default=timezone.now)

    created_date = models.DateField(default=timezone.now, db_index = True)

    device_type = models.CharField(max_length=100,null=True,blank=True)

    browser_type = models.CharField(max_length=100,null=True,blank=True)

    browser_version = models.CharField(max_length=100,null=True,blank=True)

    os_type = models.CharField(max_length=100,null=True,blank=True)

    os_version = models.CharField(max_length=100,null=True,blank=True)

    country = models.CharField(max_length=100,null=True,blank=True)

    state = models.CharField(max_length=100,null=True,blank=True)

    city = models.CharField(max_length=100,null=True,blank=True)

    latitude = models.CharField(max_length=100,null=True,blank=True)
    
    longitude = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        try:
            return self.query
        except Exception:
            return "Empty query"

    class Meta:
        verbose_name = 'SearchQueryLog'
        verbose_name_plural = 'SearchQueryLogs'

class WebsiteLinkClick(models.Model):
    link = models.TextField(db_index = True)

    search_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index = True, help_text="Selected user will see the crawled links in EasyChat console and can do searching.")    

    click_count = models.IntegerField()

    created_date = models.DateField(default=timezone.now, db_index = True)

    def __str__(self):
        try:
            return self.link
        except Exception:
            return "Empty link"

    class Meta:
        verbose_name = 'WebsiteLinkClick'
        verbose_name_plural = 'WebsiteLinkClicks'

class DailyAnalyticsReports(models.Model):
    created_date = models.DateField(default=timezone.now, db_index = True)

    search_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index = True, help_text="Selected user will see the crawled links in EasyChat console and can do searching.")    

    total_click_count = models.IntegerField()

    total_search_count = models.IntegerField()

    class Meta:
        verbose_name = 'DailyAnalyticsReports'
        verbose_name_plural = 'DailyAnalyticsReports'

    def __str__(self):
        try:
            return str(self.search_user)+" : "+str(self.created_date)
        except Exception:
            return str(self.created_date)

class DailyWorldCluodAnalytics(models.Model):
    created_date = models.DateField(default=timezone.now, db_index = True)

    search_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index = True, help_text="Selected user will see the crawled links in EasyChat console and can do searching.")    

    word_cloud_dictionary = models.TextField(
        default="[]", help_text="Word Cloud Data")

    class Meta:
        verbose_name = 'DailyWorldCluodAnalytics'
        verbose_name_plural = 'DailyWorldCluodAnalytics'

    def __str__(self):
        try:
            return str(self.search_user)+" : "+str(self.created_date)
        except Exception:
            return str(self.created_date)

class StateWiseTrafficAnalytic(models.Model):
    created_date = models.DateField(default=timezone.now, db_index = True)

    search_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index = True, help_text="Selected user will see the crawled links in EasyChat console and can do searching.")    

    state_wise_count = models.TextField(
        default="[]", help_text="State Wise Data")

    class Meta:
        verbose_name = 'StateWiseTrafficAnalytic'
        verbose_name_plural = 'StateWiseTrafficAnalytics'

    def __str__(self):
        try:
            return str(self.search_user)+" : "+str(self.created_date)
        except Exception:
            return str(self.created_date)
