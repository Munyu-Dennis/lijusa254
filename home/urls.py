from django.urls import path
from . import views
from django.conf.urls import url
from .views import (
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    WiseCreateView,
    BlogCreateView
)
urlpatterns = [
    path('', views.home, name='home'),
    path('team/', views.team, name='team'),
    path('blog/', views.blog, name='blog'), 
    path('wise/', WiseCreateView.as_view(), name='wise'),
    #path('single-blog/', views.blog_single, name='blog-single'),
    path('blog/new', BlogCreateView.as_view(), name='create-blog'),
    url(r'^blog/(?P<id>\d+)/$', views.blog_single, name='blog-single'),
    #url(r'^(?P<id>\d+)/$', BlogCreateView.as_view(), name='blog-single'),
    path('blog/<int:pk>/update', BlogUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete', BlogDeleteView.as_view(), name='blog-delete'),
] 

