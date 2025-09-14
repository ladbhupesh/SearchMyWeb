import uuid
from UserManagementApp.utils import logger_extra, logger, Validators, search_query, settings, index_website, json, get_client_ip, contry_shortname_map
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, BaseAuthentication, exceptions
from UserManagementApp.models import User, WebsiteLink, SearchQueryLog, timezone, WebsiteLinkClick, AuthToken, DailyAnalyticsReports, Sum, DailyWorldCluodAnalytics, Q, StateWiseTrafficAnalytic, Count
from django.contrib.auth.decorators import login_required
import re
from collections import Counter
import sys
import os
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework.permissions import BasePermission, IsAuthenticated

# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return 

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the username and password
        token = request.META.get('HTTP_AUTHTOKEN')

        if not token:
            return (None, None)
        try:
            auth_token = AuthToken.objects.get(uuid = token)
            user = auth_token.user
            if (timezone.now() - auth_token.last_used_at).seconds > 1800:
                auth_token.delete()
                return (None, None)
            auth_token.last_used_at = timezone.now()
            auth_token.save()
        except Exception as e:
            print(e)
            return (None, None)

        return (user, None)
    

def Logout(request):
    logout(request)
    return redirect('/login')

class GetAllWebLinksAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        weblinks = list(WebsiteLink.objects.filter(search_user=request.user).values())
        return JsonResponse(weblinks,safe = False)

GetAllWebLinks = GetAllWebLinksAPI.as_view()


class CheckAuthAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response(data={"status_code":200, "status_message":"authenticated"})

CheckAuth = CheckAuthAPI.as_view()
    

class LoginAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)

    def post(self, request):
        response = {"status_code":500, "status_message":"internal server error"}
        
        try:
            data = request.data

            username = data.get("username")
            password = data.get("password")

            errors = {}

            logger.info("LoginAPI data : %s",str(data), extra=logger_extra)
            
            user = None
            try:
                user = User.objects.get(username = username)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("LoginAPI %s at %s",str(e), str(exc_tb.tb_lineno), extra=logger_extra)
                
            try:
                if not user:
                    user = User.objects.get(email = username)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("LoginAPI %s at %s",str(e), str(exc_tb.tb_lineno), extra=logger_extra)
                errors["id_username"] = "Username or password not found"
                response['status_code'] = 301
                response['status_message'] = "Username or password not found"
                response['errors'] = errors
                logger.error("LoginAPI response %s",str(response), extra=logger_extra)
                return Response(data = response)
            
            if user.check_password(password):
                login(request, user)
                AuthToken.objects.filter(user=user).delete()
                auth_token = AuthToken.objects.create(user=user)
                response['status_code'] = 200
                response['auth_token'] = auth_token.uuid
                response['status_message'] = "Success"
                return Response(data = response)

            errors["id_username"] = "Username or password not found"
            response['status_code'] = 301
            response['status_message'] = "Username or password not found"
            response['errors'] = errors
            
            return Response(data = response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("LoginAPI %s at %s",str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        return Response(data = response)

Login = LoginAPI.as_view()

class SignUpAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)
    
    def post(self, request):
        response = {"status_code":500, "status_message":"internal server error"}
        
        try:
            data = request.data

            username = data.get("username")
            email = data.get("email")
            password1 = data.get("password1")
            password2 = data.get("password2")

            errors = {}

            validator = Validators()

            logger.info("SignUpAPI data : %s",str(data), extra=logger_extra)

            if User.objects.filter(username = username).exists():
                errors["id_username"] = "Username already exists."
                response['status_code'] = 301
                response['status_message'] = "Username already exists."
                response['errors'] = errors

            if User.objects.filter(email = email).exists():
                errors["id_email"] = "Email already exists."
                response['status_code'] = 301
                response['status_message'] = "Email already exists."
                response['errors'] = errors

            if not validator.username(username):
                errors["id_username"] = "Enter valid username"
                response['status_code'] = 301
                response['status_message'] = "Enter valid username"
                response['errors'] = errors

            if not validator.email(email):
                errors["id_email"] = "Enter valid email"
                response['status_code'] = 301
                response['status_message'] = "Enter valid email"
                response['errors'] = errors

            if password1 != password2:
                errors["password2"] = "Both passwords should match"
                response['status_code'] = 301
                response['status_message'] = "Both passwords should match"
                response['errors'] = errors

            logger.info("SignUpAPI errors : %s",str(errors), extra=logger_extra)
            if errors == {}:
                user = User.objects.create(username = username, email = email)
                user.set_password(password1)
                user.save()
                response['status_code'] = 200
                response['status_message'] = "success"
            
            return Response(data = response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SignUpAPI %s at %s",str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        return redirect('/error')

SignUp = SignUpAPI.as_view()

class StartCrawlingAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            username = request.user.username
            data = request.data
            link = data["url"]
            hyper_text = "HTTPS"  # It may change as per requirement
            index_value = "-1"  # It may change as per requirement
            username_obj = User.objects.get(username=username)
            website_obj = None
            try:
                website_obj = WebsiteLink.objects.get(
                    search_user=username_obj, link=link)
                website_obj.hyper_text = hyper_text.lower()
                website_obj.index_level = index_value
                website_obj.is_crawl = True
                website_obj.save()
            except Exception:
                website_obj = WebsiteLink.objects.create(search_user=username_obj,
                                                            link=link,
                                                            hyper_text=hyper_text.lower(),
                                                            index_level=index_value, is_crawl=True)

            response["message"] = "Save Successfully"
            response["status"] = 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error StartCrawlingAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        return Response(data=response)

StartCrawling = StartCrawlingAPI.as_view()

class SearchQueryAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, query):
        response = {}
        response["status"] = 500
        results = []
        try:
            if request.user.is_authenticated:
                user = request.user
                query_results = search_query(query, user)
                query_results = query_results['hits']['hits']
                client_ip = str(get_client_ip(request))
                device_type = "Unknown"
                browser_type = "Unknown"
                browser_version = "Unknown"
                os_type = "Unknown"
                os_version = "Unknown"
                country = "Unknown"
                state = "Unknown"
                city = "Unknown"
                latitude = "Unknown"
                longitude = "Unknown"
                if request.user_agent.is_mobile:
                    device_type = "Mobile"
                if request.user_agent.is_tablet:
                    device_type = "Tablet"
                if request.user_agent.is_pc:
                    device_type = "PC"

                try:
                    ip_to_geo = DbIpCity.get(client_ip, api_key='free')
                    country = contry_shortname_map.get(ip_to_geo.country,"Unknown")
                    city = ip_to_geo.city
                    state = ip_to_geo.region
                    latitude = ip_to_geo.latitude
                    longitude = ip_to_geo.longitude
                except Exception as E:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("RedirectUrl IP to geotools %s at %s",str(E), str(exc_tb.tb_lineno), extra=logger_extra)
                
                browser_type = request.user_agent.browser.family if request.user_agent.browser.family != None else browser_type
                browser_version = request.user_agent.browser.version_string if request.user_agent.browser.version_string != None else browser_version
                os_type = request.user_agent.os.family if request.user_agent.os.family != None else os_type
                os_version = request.user_agent.os.version_string if request.user_agent.os.version_string != None else os_version

                for query_result in query_results:
                    results.append({
                        'id':query_result['_id'],
                        'title':query_result['_source']['title'].replace("\r","").replace("\t","").replace("\n",""),
                        'description':query_result['_source']['description'].replace("\r","").replace("\t","").replace("\n","")[:500],
                        'link':settings.HOST_URL + '/search/redirect/' +str(query_result['_id']),
                    })
                response["message"] = "Save Successfully"
                response["query_result"] = results
                response["status"] = 200
                SearchQueryLog.objects.create(
                        query = query,
                        result = results, 
                        search_user = user,
                        device_type = device_type, 
                        browser_type = browser_type, 
                        browser_version = browser_version, 
                        os_type = os_type, 
                        os_version = os_version, 
                        country = country, 
                        state = state, 
                        city = city, 
                        latitude = latitude, 
                        longitude = longitude
                    )
                return Response(data=response)
            response["message"] = "UnAuthorised"
            response["status"] = 403
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error SearchQueryAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        
        SearchQueryLog.objects.create(
                        query = query,
                        result = results, 
                        search_user = user,
                        device_type = device_type, 
                        browser_type = browser_type, 
                        browser_version = browser_version, 
                        os_type = os_type, 
                        os_version = os_version, 
                        country = country, 
                        state = state, 
                        city = city, 
                        latitude = latitude, 
                        longitude = longitude
                    )
        return Response(data=response)

SearchQuery = SearchQueryAPI.as_view()

def SearchRedirect(request, url_pk):
    try:
        website_url_obj = WebsiteLink.objects.get(pk=int(url_pk))
        website_url_obj.click_count = website_url_obj.click_count + 1
        website_url_obj.save()
        click_obs = WebsiteLinkClick.objects.filter(search_user = website_url_obj.search_user,link = website_url_obj.link, created_date = timezone.now().date())
        if click_obs:
            click_obs = click_obs[0]
            click_obs.click_count +=1
            click_obs.save()
        else:
            WebsiteLinkClick.objects.create(search_user = website_url_obj.search_user, link = website_url_obj.link, click_count = 1)
        return redirect(str(website_url_obj.link))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("SearchRedirect: %s at %s", e, str(
            exc_tb.tb_lineno), extra={'AppName': 'EasySearch'})
        return render(request, 'EasySearchApp/error_500.html')


class GetTraficSourcesListAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        weblinks = list(WebsiteLink.objects.filter(~Q(click_count=0),search_user=request.user).order_by('-click_count').values('link', 'click_count', 'last_indexed'))
        return JsonResponse(weblinks,safe = False)

GetTraficSourcesList = GetTraficSourcesListAPI.as_view()

class GetManageIndexesListAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        weblinks = list(WebsiteLink.objects.filter(search_user=request.user, is_indexed=True).order_by('-click_count').values('link', 'id', 'last_indexed'))
        return JsonResponse(weblinks,safe = False)

GetManageIndexesList = GetManageIndexesListAPI.as_view()

class ManageIndexAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, link_id):
        response = {}
        response["status"] = 500
        try:
            if request.user.is_authenticated:
                user = request.user
                web_link = WebsiteLink.objects.get(search_user=request.user, pk = link_id)
                settings.ELASTIC_SEARCH_OBJ.delete(index = user.uuid,id = link_id)
                web_link.delete()
                response["message"] = "Save Successfully"
                response["status"] = 200
                return Response(data=response)
            response["message"] = "UnAuthorised"
            response["status"] = 403
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error SearchQueryAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        return Response(data=response)

    def put(self, request, link_id):
        response = {}
        response["status"] = 500
        try:
            if request.user.is_authenticated:
                user = request.user
                web_link = WebsiteLink.objects.get(search_user=request.user, pk = link_id)         
                index_website(web_link)       
                response["message"] = "Save Successfully"
                response["status"] = 200
                return Response(data=response)
            response["message"] = "UnAuthorised"
            response["status"] = 403
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error SearchQueryAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        return Response(data=response)

ManageIndex = ManageIndexAPI.as_view()    

class GetAnalyticsDetailsAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        start_date = timezone.now().date() - timezone.timedelta(days=7)
        end_date = timezone.now().date()
        try:
            str_start_date = request.GET.get('start_date')
            str_end_date = request.GET.get('end_date')
            start_date = timezone.datetime.strptime(str_start_date,"%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(str_end_date,"%Y-%m-%d").date()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error GetAnalyticsDetails: %s at %s",
                            str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        analytics_details = list(DailyAnalyticsReports.objects.filter(search_user=request.user,created_date__gte=start_date,created_date__lte=end_date,).values('created_date', 'total_click_count', 'total_search_count'))
        today = timezone.now().date()
        if end_date >= today:
            total_click_count = WebsiteLinkClick.objects.filter(search_user = request.user,created_date=today).aggregate(Sum('click_count'))['click_count__sum']
            if total_click_count==None:
                total_click_count=0
            total_search_count = SearchQueryLog.objects.filter(search_user = request.user, created_date=today).count()
            analytics_details.append({'created_date':today,'total_click_count': total_click_count, 'total_search_count':total_search_count})
        return JsonResponse(analytics_details,safe = False)


GetAnalyticsDetails = GetAnalyticsDetailsAPI.as_view()
class WrodCloudDetailsAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        start_date = timezone.now().date() - timezone.timedelta(days=7)
        end_date = timezone.now().date()
        try:
            str_start_date = request.GET.get('start_date')
            str_end_date = request.GET.get('end_date')
            start_date = timezone.datetime.strptime(str_start_date,"%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(str_end_date,"%Y-%m-%d").date()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error GetAnalyticsDetails: %s at %s",
                            str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        analytics_details = list(DailyWorldCluodAnalytics.objects.filter(search_user=request.user,created_date__gte=start_date,created_date__lte=end_date,).values('created_date', 'word_cloud_dictionary'))
        today = timezone.now().date()
        if end_date >= today:
            total_search = SearchQueryLog.objects.filter(search_user = request.user, created_date=today).values_list("query", flat=True)
            word_list = re.sub('[^A-Za-z]+', ' ',  ' '.join(list(total_search))).split(" ")
            word_list = [x for x in word_list if not x.strip().isdigit()]
            word_cloud_dictionary = json.dumps(dict(Counter(word_list)))
            analytics_details.append({'created_date':today,'word_cloud_dictionary': word_cloud_dictionary})
        return JsonResponse(analytics_details,safe = False)

WrodCloudDetails = WrodCloudDetailsAPI.as_view()

class GetLiveLoggerAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        logs = []
        with open(settings.APP_LOG_FILENAME,'r') as f:
            logs = f.read().splitlines()[-100:]
        return JsonResponse(logs,safe = False)

GetLiveLogger = GetLiveLoggerAPI.as_view()

@login_required()
def GetCodeSnippet(request):
    logs = []
    with open(settings.APP_LOG_FILENAME,'r') as f:
        logs = f.read().splitlines()[-100:]
    return JsonResponse(logs,safe = False)

class SelectSearchPageAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            deploy_js_path = settings.MEDIA_ROOT+"deploy/"+str(request.user.uuid)+".js" 
            if not os.path.exists(deploy_js_path):
                base_file = open(settings.BASE_DIR+"/UserManagementApp/static/UserManagementApp/js/select-search.js","r").read()
                base_file = base_file.replace("/search/'+current_selected_text",f"{settings.HOST_URL}/search/{request.user.uuid}/'+current_selected_text")
                f = open(deploy_js_path,'w')
                f.write(base_file)
            deploy_js_link = settings.HOST_URL+"/files/deploy/"+str(request.user.uuid)+".js" 
            return Response(data = {"status_code":200,"status_message":"success","deploy_js_link":deploy_js_link})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error SelectSearchPageAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        return Response(data = {"status_code":500,"status_message":"Internal server error."})


SelectSearchPage = SelectSearchPageAPI.as_view()

class SelectSearchQueryAPI(APIView):

    def get(self, request, uuid, query):
        response = {}
        response["status"] = 500
        results = []
        try:
            user = User.objects.filter(uuid=uuid)
            if user:
                client_ip = str(get_client_ip(request))
                device_type = "Unknown"
                browser_type = "Unknown"
                browser_version = "Unknown"
                os_type = "Unknown"
                os_version = "Unknown"
                country = "Unknown"
                state = "Unknown"
                city = "Unknown"
                latitude = "Unknown"
                longitude = "Unknown"
                if request.user_agent.is_mobile:
                    device_type = "Mobile"
                if request.user_agent.is_tablet:
                    device_type = "Tablet"
                if request.user_agent.is_pc:
                    device_type = "PC"

                try:
                    ip_to_geo = DbIpCity.get(client_ip, api_key='free')
                    country = contry_shortname_map.get(ip_to_geo.country,"Unknown")
                    city = ip_to_geo.city
                    state = ip_to_geo.region
                    latitude = ip_to_geo.latitude
                    longitude = ip_to_geo.longitude
                except Exception as E:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error("RedirectUrl IP to geotools %s at %s",str(E), str(exc_tb.tb_lineno), extra=logger_extra)
                
                browser_type = request.user_agent.browser.family if request.user_agent.browser.family != None else browser_type
                browser_version = request.user_agent.browser.version_string if request.user_agent.browser.version_string != None else browser_version
                os_type = request.user_agent.os.family if request.user_agent.os.family != None else os_type
                os_version = request.user_agent.os.version_string if request.user_agent.os.version_string != None else os_version

                user = user[0]
                query_results = search_query(query, user)
                query_results = query_results['hits']['hits']
                for query_result in query_results:
                    results.append({
                        'id':query_result['_id'],
                        'title':query_result['_source']['title'].replace("\r","").replace("\t","").replace("\n",""),
                        'description':query_result['_source']['description'].replace("\r","").replace("\t","").replace("\n","")[:500],
                        'link':settings.HOST_URL + '/search/redirect/' +str(query_result['_id']),
                    })
                response["message"] = "Save Successfully"
                response["query_result"] = results
                response["status"] = 200
                SearchQueryLog.objects.create(
                        query = query,
                        result = results, 
                        search_user = user,
                        device_type = device_type, 
                        browser_type = browser_type, 
                        browser_version = browser_version, 
                        os_type = os_type, 
                        os_version = os_version, 
                        country = country, 
                        state = state, 
                        city = city, 
                        latitude = latitude, 
                        longitude = longitude
                    )
                return Response(data=response)
            response["message"] = "UnAuthorised"
            response["status"] = 403
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error SelectSearchQueryAPI: %s at %s",
                         str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        
        SearchQueryLog.objects.create(
                        query = query,
                        result = results, 
                        search_user = user,
                        device_type = device_type, 
                        browser_type = browser_type, 
                        browser_version = browser_version, 
                        os_type = os_type, 
                        os_version = os_version, 
                        country = country, 
                        state = state, 
                        city = city, 
                        latitude = latitude, 
                        longitude = longitude
                    )
        return Response(data=response)

SelectSearchQuery = SelectSearchQueryAPI.as_view()
  

class GetStateWiseTraficAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        start_date = timezone.now().date() - timezone.timedelta(days=7)
        end_date = timezone.now().date()
        try:
            str_start_date = request.GET.get('start_date')
            str_end_date = request.GET.get('end_date')
            start_date = timezone.datetime.strptime(str_start_date,"%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(str_end_date,"%Y-%m-%d").date()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Error GetStateWiseTrafic: %s at %s",
                            str(e), str(exc_tb.tb_lineno), extra=logger_extra)
        state_wise_traffic = list(StateWiseTrafficAnalytic.objects.filter(search_user=request.user,created_date__gte=start_date,created_date__lte=end_date,).values('state_wise_count'))
        
        today = timezone.now().date()
        if end_date >= today:
            state_wise_count = SearchQueryLog.objects.filter(search_user = request.user, created_date=today).values('state').order_by("state").annotate(frequency=Count("state"))
            state_wise_count = json.dumps(list(state_wise_count))
            state_wise_traffic.append({'state_wise_count': state_wise_count})
        return JsonResponse(state_wise_traffic,safe = False)

GetStateWiseTrafic = GetStateWiseTraficAPI.as_view()
        
GetTraficSourcesList = GetTraficSourcesListAPI.as_view()

def handler404(request, exception):
    return render(request,'UserManagementApp/40X.html')


def handler500(request):
    return render(request,'UserManagementApp/50X.html')
