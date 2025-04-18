from django.urls import path

from client.apps import ClientConfig
from client.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView

app_name = ClientConfig.name


urlpatterns = [
    path('', ClientListView.as_view(), name='clients_list'),
    path('create/', ClientCreateView.as_view(), name='clients_create'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='clients_update'),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name='clients_delete'),
    path('more/<int:pk>', ClientDetailView.as_view(), name='clients_more'),
]
