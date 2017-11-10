from django.conf.urls import url
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import login, logout
from app.views import send_morsel, start_hunt, MorselList, MorselDetailView, register, create_morsel

app_name = 'app'
urlpatterns = [
    url(r'^$', lambda r: redirect('/app/morsels/')),
    url(r'^morsels/$', MorselList.as_view(), name='morsel_list'),
    url(r'^morsels/send/$', send_morsel, name='morsel_send'),
    url(r'^morsels/(?P<morsel_id>[0-9])/start_hunt/$', start_hunt, name='start_hunt'),
    url(r'^register/', register),
    url(r'^morsels/create/$', create_morsel, name="create_morsel"),
    url(r'^morsels/(?P<pk>[0-9])/display$', MorselDetailView.as_view(), name='morsel_detail')
]