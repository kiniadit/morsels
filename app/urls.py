from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from app.views import send_morsel, start_hunt, MorselList, MorselDetailView

app_name = 'app'
urlpatterns = [
    url(r'^morsels/$', MorselList.as_view(), name='list_morsels'),
    url(r'^morsels/send/$', send_morsel, name='send_morsel'),
    url(r'^morsels/(?P<morsel_id>[0-9])/start_hunt/$', start_hunt, name='start_hunt'),
    url(r'^morsels/(?P<pk>[0-9])/display$', MorselDetailView.as_view(), name='morsel_detail')
]