import urllib, requests

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.conf import settings
from django.shortcuts import redirect

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError

def make_flow(request):
    host = request.META.get('HTTP_HOST', 'mattlong.org')
    print host
    print request.META
    flow = OAuth2WebServerFlow(
            client_id=settings.GOOGLE_API_CLIENT_ID,
            client_secret=settings.GOOGLE_API_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/userinfo.email',
            redirect_uri='http://%s/oauth2callback' % (host,))
    flow.redirect_uri='http://%s/oauth2callback' % (host,)
    return flow

def oauth_login(request):
    flow = make_flow(request)
    oauth_url = urllib.unquote(flow.step1_get_authorize_url())
    return redirect(oauth_url, permanent=False)

def oauth_callback(request):
    try:
        code = request.GET['code']
    except KeyError:
        return HttpResponse('oauth code not found')

    try:
        flow = make_flow(request)
        creds = flow.step2_exchange(code)
        access_token = creds.access_token
    except FlowExchangeError, ex:
        return HttpResponse('error getting oauth credentials')

    try:
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % (access_token,))
        email = r.json['email']
        email = settings.OAUTH_EMAIL_MAP.get(email, email)

        user = User.objects.get(email=email)
        user.backend = 'django.contrib.auth.backends.ModelBackend' #this must be filled in, hackity-hack
        login(request, user)
    except User.DoesNotExist, ex:
        return HttpResponse('%s is not authorized' % (email,))
    except Exception, ex:
        return HttpResponse('error authenticating %s' % (email,))

    return redirect('/', permanent=False)
