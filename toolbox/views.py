import requests

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.conf import settings

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError

def oauth_callback(request):
    try:
        code = request.GET['code']
    except KeyError:
        print request.GET
        return HttpResponse("code not found")

    try:
        flow = OAuth2WebServerFlow(
                client_id=settings.GOOGLE_API_CLIENT_ID,
                client_secret=settings.GOOGLE_API_CLIENT_SECRET,
                scope='https://www.googleapis.com/auth/userinfo.email')
        flow.redirect_uri='http://localhost:8000/oauth2callback'
        creds = flow.step2_exchange(code)
    except FlowExchangeError, ex:
        #return HttpResponse(ex.message, status=400)

        access_token = settings.OAUTH_DEBUG_ACCESS_TOKEN

    try:
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % (access_token,))
        email = r.json['email']
        email = settings.OAUTH_EMAIL_MAP.get(email, email)

        user = User.objects.get(email=email)
        user.backend = 'django.contrib.auth.backends.ModelBackend' #this must be filled in, hackity-hack
    except Exception, ex:
        return HttpResponse(str(ex))

    login(request, user)

    return HttpResponse(user.email)
