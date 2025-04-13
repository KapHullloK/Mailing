from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, HomePageView

app_name = BlogConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='blog_home'),
    path('all/', BlogListView.as_view(), name='blog_list'),
    path('more/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('update/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
]
