import sys
import operator

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from UserManagementApp.models import *


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(index_website_scheduler, 'interval', seconds=10)
    scheduler.add_job(crawl_website_scheduler, 'interval', seconds=5)
    scheduler.start()


def index_website_scheduler():
    from UserManagementApp.utils import index_website, logger, logger_extra
    from UserManagementApp.models import WebsiteLink
    import sys
    try:
        logger.info("STARTED index_website_scheduler",extra=logger_extra)
        website_link_objs = WebsiteLink.objects.filter(is_indexed=False)
        for website_link_obj in website_link_objs:
            logger.info(website_link_obj.link, extra=logger_extra)
            index_website(website_link_obj)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error index_website_scheduler %s at %s",
                     str(e), str(exc_tb.tb_lineno), extra=logger_extra)


def crawl_website_scheduler():
    from UserManagementApp.utils import crawl_weblink, logger, logger_extra
    from UserManagementApp.models import WebsiteLink
    import sys
    try:
        logger.info("STARTED crawl_website_scheduler",extra=logger_extra)
        website_link_obj = WebsiteLink.objects.filter(
            is_crawl=True).exclude(index_level=None).first()
        if website_link_obj:
            website_link_obj.is_crawl = False
            website_link_obj.save()
            crawl_weblink(website_link_obj, WebsiteLink, User)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Error crawl_website_scheduler %s at %s",
                     str(e), str(exc_tb.tb_lineno), extra=logger_extra)
