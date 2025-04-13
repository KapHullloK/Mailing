from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('', cache_page(60)(MessageListView.as_view()), name='message_list'),
    path('create/', MessageCreateView.as_view(), name='message_create'),
    path('update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
]
