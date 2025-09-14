import logging
from UserManagementApp.constants import *
import re
import sys
from django.conf import settings
import requests
import os
import json
from bs4 import BeautifulSoup

from lxml import html
from urllib.parse import urljoin
import tldextract
import textract
import urllib.request
from django.utils import timezone
from urllib.parse import unquote, urlparse

logger = logging.getLogger(__name__)

class Validators:

    def username(self,username):
        if username.isalpha():
            return True
        return False

    def email(self,email):
        regex = r'\b[A-Za-z0-9.~_%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        return False

    def mobile(self,mobile):
        mobile = str(mobile)
        if len(mobile) == 10:
            if re.match(r"[6-9][0-9]{9}", mobile):
                return True
        return False

def search_query(query, user):
    # Searching on the basis on "description"
    try:
        result = ''
        uuid = user.uuid
        result = settings.ELASTIC_SEARCH_OBJ.search(index=uuid, body={'query':
                                                                                         {'match':
                                                                                          {
                                                                                              'description': query
                                                                                          }
                                                                                          }
                                                                                         })
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("search_query: %s at %s", e, str(exc_tb.tb_lineno), extra=logger_extra)
    return result



"""
function: get_website_title

Getting website "title"
"""


def get_website_title(response_soup):
    try:
        title = response_soup.select('title')
        title = title[0].text
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("get_website_title: %s at %s", e, str(exc_tb.tb_lineno), extra=logger_extra)
        return ""
    return title


"""
function: get_meta_keywords

Getting website ""keywords" in meta tags
"""


def get_meta_keywords(response_soup):
    try:
        meta = response_soup.find_all('meta')
        keywords = ""
        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in 'keywords':
                keywords = tag.attrs['content']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("get_meta_keywords: %s at %s", e, str(exc_tb.tb_lineno), extra=logger_extra)
        return ""
    return keywords


"""
function: get_meta_description

Getting website "description" in meta tag
"""


def get_meta_description(response_soup):
    try:
        meta = response_soup.find_all('meta')
        description = ""
        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in 'description':
                description = tag.attrs['content']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("get_meta_description: %s at %s",
                     e, str(exc_tb.tb_lineno), extra=logger_extra)
        return ""
    return description


"""
function: index_website
input params:
            website_url_obj (mandatory)

Indexing of the website
"""


def index_website(website_url_obj):
    from UserManagementApp.models import WebsiteLink
    try:
        response = requests.get(website_url_obj.link, timeout=10)
        if response.status_code != 200:
            logger.error(f"index_website: url not found : {website_url_obj.link}", extra=logger_extra)
            website_url_obj.delete()
            return
        if response.url != website_url_obj.link.strip() and WebsiteLink.objects.all().exclude(pk=website_url_obj.pk).filter(link=response.url,is_indexed=True):
            logger.error(f"Page leading to already indexed url : {website_url_obj.link}", extra=logger_extra)
            website_url_obj.delete()
            return

        """
        Checking the content type of the website link
            1. HTML Page: 'text/html'
            2. PDF: 'application/pdf'
            3. Image: 'text/html; charset=iso-8859-1'
        """
        content_type = response.headers.get('content-type')
        if 'text/html' in content_type:
            soup = BeautifulSoup(response.text, "html.parser")

            # Getting all the paragraph.
            paragraph_texts = soup.select('p')

            # Getting the title.
            title = get_website_title(soup)

            # Getting the ketword.
            keywords = get_meta_keywords(soup)
            if(keywords == ""):
                keywords = title
            # Getting description.
            description = get_meta_description(soup)
            if(description == ""):
                description = title

            # IMPROVING SERCH RESULT

            description = str(description + " " + keywords + " " + title)

            texts = ""
            for paragraph_text in paragraph_texts:
                texts += paragraph_text.text
            texts = texts.split(" ")

            saturated_text = ""
            for text in texts:
                if(text not in STOP_WORDS):
                    saturated_text += text
                    saturated_text += " "

            # Content
            saturated_text = description + " " + keywords + " " + saturated_text + " " + title
            username = website_url_obj.search_user.uuid

            logger.info("uuid: %s", username, extra=logger_extra)

            # Create file if not exist
            if not os.path.exists('files/' + str(username)):
                os.makedirs("files/" + str(username))

            # Storing INDEX

            with open("files/" + str(username) + "/indexed-data-" + str(website_url_obj.pk) + ".json", "w") as fp:
                logger.info("file saved", extra=logger_extra)
                json.dump({'type': 'html', 'name': str(username), 'content': saturated_text, 'url': website_url_obj.link,
                           'title': title, 'url_pk': website_url_obj.pk, 'keywords': keywords, 'description': description}, fp)

            # Getting index data
            read_file = open("files/" + str(username) +
                             "/indexed-data-" + str(website_url_obj.pk) + ".json", 'r')
            data = json.load(read_file)
            logger.info(website_url_obj.pk, extra=logger_extra)

            # Doing Indexing in ElasticSearch
            settings.ELASTIC_SEARCH_OBJ.index(
                index=username, id=int(website_url_obj.pk), document=data)

        elif 'application/pdf' in content_type:

            logger.info("[PDF] document in %s", website_url_obj.link, extra=logger_extra)

            try:
                request_response = requests.get(website_url_obj.link, stream=True)

                logger.info("%s is active url %s",
                            website_url_obj.link, str(request_response.status_code), extra=logger_extra)

                username = website_url_obj.search_user.uuid

                if not os.path.exists('documents/' + str(username)):
                    os.makedirs("documents/" + str(username))

                open("documents/" + str(username) + "/document-data-" +
                     str(website_url_obj.pk) + ".pdf", "wb").write(response.content)

                file_text_pdf = ""
                file_name = str("documents/" + str(username) +
                                "/document-data-" + str(website_url_obj.pk) + ".pdf")
                file_text_pdf = str(
                    (textract.process(file_name)).decode('ascii', 'ignore'))

                if not os.path.exists('files/' + str(username)):
                    os.makedirs("files/" + str(username))

                title = ""
                title = website_url_obj.link
                title = title.split("/")[-1]
                title = urllib.request.unquote(title)

                file_text_pdf = str(title + " " + file_text_pdf)
                with open("files/" + str(username) + "/document-data-" + str(website_url_obj.pk) + ".json", "w") as fp:
                    json.dump({'type': 'pdf', 'name': str(username), 'content': file_text_pdf, 'url': website_url_obj.link,
                               'title': title, 'url_pk': website_url_obj.pk, 'keywords': file_text_pdf, 'description': file_text_pdf}, fp)
                read_file = open(
                    "files/" + str(username) + "/document-data-" + str(website_url_obj.pk) + ".json", 'r')
                data = json.load(read_file)

                settings.ELASTIC_SEARCH_OBJ.index(
                    index=username, id=int(website_url_obj.pk), document=data)

            except Exception as es:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("index_website: %s at %s",
                             es, str(exc_tb.tb_lineno), extra=logger_extra)

        website_url_obj.is_indexed = True
        website_url_obj.last_indexed = timezone.now()
        website_url_obj.save()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("index_website: %s at %s", e, str(exc_tb.tb_lineno), extra=logger_extra)
        #website_url_obj.is_indexed = True
        #website_url_obj.save()


"""
function: create_websitelink
input params:
            website_url_obj (mandatory)
            parsed_url (mandatory)
            WebsiteLink (mandatory)
"""


def create_websitelink(website_url_obj, parsed_url, WebsiteLink):
    hyper_link = website_url_obj.hyper_text
    user_obj = website_url_obj.search_user
    parsed_url = parsed_url.strip()
    try:
        WebsiteLink.objects.get(link=str(parsed_url))
        logger.info("website matching url already exist.", extra=logger_extra)
    except Exception:
        logger.warning("website matching url doesn't exist. Creating new", extra=logger_extra)
        WebsiteLink.objects.create(link=str(parsed_url),
                                   search_user=user_obj,
                                   #is_crawl = True,
                                   #index_level = -1,
                                   hyper_text=str(hyper_link))
    except Exception:
        logger.error("Trying to create dumplicate link", extra=logger_extra)


"""
function: EasySearchCrawler

"""


class EasySearchCrawler:

    def __init__(self, start_page):
        self.visited_url = {}
        self.queue_url = [start_page]

    def get_url_list(self, website_url_obj, url, WebsiteLink):
        try:
            domain_name = tldextract.extract(url)
            domain = domain_name.domain
            suffix = domain_name.suffix
            if str(website_url_obj.hyper_text) in url:
                domain = str(domain) + "." + str(suffix)
                print(str(domain) in url)
                if str(domain) in url:
                    try:
                        parsed_html = ""
                        url = url.lower()
                        response = requests.get(url, timeout=10.0)
                        raw_html = response.text
                        parsed_html = html.fromstring(raw_html)
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        logger.error("EasySearchCrawler: get_url_list: %s at line no %s", str(
                            e), str(exc_tb.tb_lineno), extra=logger_extra)

                    url_title_item = parsed_html.xpath('//title')
                    url_title = '(NO TITLE)'
                    try:
                        url_title = url_title_item[0].text
                    except Exception:
                        url_title = '(ERROR TITLE)'

                    self.visited_url[url] = url_title

                    for a_tag in parsed_html.xpath('//a'):
                        raw_url = a_tag.get('href')
                        if raw_url is None:
                            continue
                        parsed_url = urljoin(url, raw_url)

                        if str(domain) not in parsed_url:
                            continue
                        parsed_url_link = urlparse(parsed_url)
                        parsed_url = parsed_url_link.scheme + "://" + parsed_url_link.netloc + parsed_url_link.path
                        if parsed_url not in list(self.visited_url.keys()) and parsed_url not in self.queue_url:
                            if str(website_url_obj.hyper_text).lower() == parsed_url_link.scheme:
                                if parsed_url_link.netloc == urlparse(url).netloc:
                                    self.queue_url.append(parsed_url)
                                    create_websitelink(
                                        website_url_obj, parsed_url, WebsiteLink)
                else:
                    logger.info("Ignoring this url: %s ", url, extra=logger_extra)
            else:
                logger.info("Ignoring this url: %s ", website_url_obj.hyper_text, extra=logger_extra)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("get_url_list: %s at %s", e, str(exc_tb.tb_lineno), extra=logger_extra)

    def start_crawler(self, website_url_obj, index_level, WebsiteLink):
        try:
            while index_level != 0:
                this_url = self.queue_url[0]
                self.get_url_list(website_url_obj, this_url, WebsiteLink)

                if len(self.queue_url) == 1:
                    break
                else:
                    self.queue_url = self.queue_url[1:]
                index_level -= 1

            logger.info("Crwaling is completed.", extra=logger_extra)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("start_crawler: %s at %s", e, str(exc_tb.tb_lineno), extra=logger_extra)


"""
function: crawl_weblink
input params:
            website_url_obj (mandatory)
            WebsiteLink(mandatory)
            SearchUser(mandatory)

"""


def crawl_weblink(website_url_obj, WebsiteLink, SearchUser):
    try:
        crawl_obj = EasySearchCrawler(website_url_obj.link)
        crawl_obj.start_crawler(
            website_url_obj, website_url_obj.index_level, WebsiteLink)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("crawl_weblink: %s at %s", e, str(exc_tb.tb_lineno), extra=logger_extra)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
