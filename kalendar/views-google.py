from django.shortcuts import render
from django.views.generic import ListView
from classsite.views import URLMixin
from .models import Kalendar, CredentialsModel
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage
from oauth2client import tools
from django.http import HttpResponseRedirect

client_id = "263679544817-q03afh4k0afir9q38qpnede8qk3764q2.apps.googleusercontent.com"
client_secret = "FypaA281QVtdKPaFDhGJERFF"
redirect_uris="http://127.0.0.1:8000/oauth2callback"
scope = 'https://www.googleapis.com/auth/calendar'
flow = OAuth2WebServerFlow(client_id, client_secret, scope, redirect_uris) 

def index (request, class_url):

    auth_uri=flow.step1_get_authorize_url()
    return HttpResponseRedirect(auth_uri)
        
# class KalendarListView(URLMixin, ListView): 
#     template_name="kalendar/kalendar_list.html"
#     context_object_name='kalendar_list'
#     model=Kalendar


def auth_return(request):
    code=request.GET["code"]
    credential=flow.step2_exchange(code)
    storage=Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    
    