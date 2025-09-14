def cronjob():
    from UserManagementApp.models import User, SearchQueryLog, timezone, WebsiteLinkClick, WebsiteLink, DailyAnalyticsReports, logger, logger_extra, Sum, DailyWorldCluodAnalytics, StateWiseTrafficAnalytic, Count
    import re
    from collections import Counter
    import sys
    import json
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    try:
        if DailyAnalyticsReports.objects.all().count() != 0:
                last_date = DailyAnalyticsReports.objects.latest(
                    'created_date').created_date
        else:
            last_date = SearchQueryLog.objects.all().order_by('-created_date').last().created_date
        today = timezone.now()
        while(last_date < today.date()):
            for user in User.objects.all():
                total_search_count = SearchQueryLog.objects.filter(search_user = user, created_date=last_date).count()
                total_click_count = WebsiteLinkClick.objects.filter(search_user = user,created_date=last_date).aggregate(Sum('click_count'))['click_count__sum']
                if total_click_count==None:
                    total_click_count = 0
                if DailyAnalyticsReports.objects.filter(search_user = user, created_date=last_date):
                    pass
                else:
                    DailyAnalyticsReports.objects.create(
                            search_user = user, 
                            created_date=last_date,
                            total_click_count = total_click_count,
                            total_search_count = total_search_count
                        )
            last_date = last_date + timezone.timedelta(days=1)

        if DailyWorldCluodAnalytics.objects.all().count() != 0:
                last_date = DailyWorldCluodAnalytics.objects.latest(
                    'created_date').created_date
        else:
            last_date = SearchQueryLog.objects.all().order_by('-created_date').last().created_date
        today = timezone.now()
        while(last_date < today.date()):
            for user in User.objects.all():
                total_search = SearchQueryLog.objects.filter(search_user = user, created_date=last_date).values_list("query", flat=True)
                word_list = re.sub('[^A-Za-z]+', ' ',  ' '.join(list(total_search))).split(" ")
                word_list = [x for x in word_list if not x.strip().isdigit()]
                stop_words = set(stopwords.words('english'))
                word_list = [w for w in word_list if not w.lower() in stop_words]
                word_cloud_dictionary = json.dumps(dict(Counter(word_list)))
                if DailyWorldCluodAnalytics.objects.filter(search_user = user, created_date=last_date):
                    pass
                else:
                    DailyWorldCluodAnalytics.objects.create(
                            search_user = user, 
                            created_date=last_date,
                            word_cloud_dictionary=word_cloud_dictionary
                        )
            last_date = last_date + timezone.timedelta(days=1)

        if StateWiseTrafficAnalytic.objects.all().count() != 0:
                last_date = StateWiseTrafficAnalytic.objects.latest(
                    'created_date').created_date
        else:
            last_date = SearchQueryLog.objects.all().order_by('-created_date').last().created_date
        today = timezone.now()
        while(last_date < today.date()):
            for user in User.objects.all():
                state_wise_count = SearchQueryLog.objects.filter(search_user = user, created_date=last_date).values('state').order_by("state").annotate(frequency=Count("state"))
                state_wise_count = json.dumps(list(state_wise_count))
                if StateWiseTrafficAnalytic.objects.filter(search_user = user, created_date=last_date):
                    pass
                else:
                    StateWiseTrafficAnalytic.objects.create(
                            search_user = user, 
                            created_date=last_date,
                            state_wise_count=state_wise_count
                        )
            last_date = last_date + timezone.timedelta(days=1)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("Analytics! %s at %s", str(e), str(exc_tb.tb_lineno), extra=logger_extra)
