from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import MailListView, MailCreateView, MailUpdateView, MailDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('', cache_page(60)(MailListView.as_view()), name='mail_list'),
    path('create/', MailCreateView.as_view(), name='mail_create'),
    path('update/<int:pk>', MailUpdateView.as_view(), name='mail_update'),
    path('delete/<int:pk>', MailDeleteView.as_view(), name='mail_delete'),
]
