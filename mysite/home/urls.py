from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from blog.models import Post


urlpatterns = patterns('',
                        url(r'^home/$', ListView.as_view(
                            queryset=Post.objects.all().order_by("-date"),
                            template_name="home.html")),

                        url(r'^datasets/$', ListView.as_view(
                            queryset=Post.objects.all().order_by("-date"),
                            template_name="datasets.html")),

                        url(r'^maps/$', ListView.as_view(
                            queryset=Post.objects.all().order_by("-date"),
                            template_name="maps.html")),

                        url(r'^about/$', ListView.as_view(
                            queryset=Post.objects.all().order_by("-date"),
                            template_name="about.html")),

                        url(r'^.*/$', ListView.as_view(
                            queryset=Post.objects.all().order_by("-date"),
                            template_name="home.html")),




)

