from django.contrib import admin
from django.urls import path
from UserManagementApp.views import *
from UserManagementApp import crawl_website

urlpatterns = [
    path('login', Login, name="login"),
    path('check-auth', CheckAuth, name="check-auth"),
    path('signup', SignUp, name="signup"),
    path('logout', Logout, name="logout"),
    path('start-crawling', StartCrawling, name="start-crawling"),
    path('get-all-web-links', GetAllWebLinks, name="get-all-web-links"),
    path('search/<str:query>', SearchQuery, name="search"),
    path('search/<uuid:uuid>/<str:query>', SelectSearchQuery, name="search"),
    path('search/redirect/<int:url_pk>', SearchRedirect, name='search-redirect'),
    path('get-trafic-sources-list', GetTraficSourcesList, name='get-trafic-sources-list'),
    path('get-manage-indexes-list', GetManageIndexesList, name='get-manage-indexes-list'),
    path('manage-index/<int:link_id>', ManageIndex, name='manage-index'),
    path('analytics-details', GetAnalyticsDetails, name='analytics-details'),
    path('wordcloud-details', WrodCloudDetails, name='wordcloud-details'),
    path('get-live-logger', GetLiveLogger, name='get-live-logger'),
    path('get-code-snippet', GetCodeSnippet, name='get-code-snippet'),
    path('select-search', SelectSearchPage, name='select-search'),
    path('get-state-wise-traffic', GetStateWiseTrafic, name='get-state-wise-traffic'),
]

#crawl_website.start_scheduler()
