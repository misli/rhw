"""rhw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required as lr, permission_required as pr
from django.contrib.auth.views import login, logout

from .views import *
from .forms import PasswordResetForm

urlpatterns = [
    url(r'^$',                                              HomeView.as_view(),                 name='home'),
    url(r'^ideas/$',                                        IdeasView.as_view(),                name='ideas'),
    url(r'^ideas/new/$',                                    lr(IdeaCreateView.as_view()),       name='idea-create'),
    url(r'^ideas/(?P<slug>[^/]+)/$',                        IdeaView.as_view(),                 name='idea'),
    url(r'^ideas/(?P<slug>[^/]+)/edit/$',                   lr(IdeaEditView.as_view()),         name='idea-edit'),
    url(r'^ideas/(?P<slug>[^/]+)/(?P<op>[+-])1$',           lr(interested),                     name='interested'),
    url(r'^projects/$',                                     ProjectsView.as_view(),             name='projects'),
    url(r'^projects/(?P<slug>[^/]+)/$',                     ProjectView.as_view(),              name='project'),
    url(r'^projects/(?P<slug>[^/]+)/edit/$',                lr(ProjectEditView.as_view()),      name='project-edit'),
    url(r'^projects/(?P<slug>[^/]+)/(?P<op>[+-])1$',        lr(member_vote),                    name='member_vote'),
    url(r'^rhws/$',                                         RhwsView.as_view(),                 name='rhws'),
    url(r'^rhws/new/$',                                     pr('')(RhwCreateView.as_view()),    name='rhw-create'),
    url(r'^rhws/(?P<slug>[^/]+)/$',                         RhwView.as_view(),                  name='rhw'),
    url(r'^rhws/(?P<slug>[^/]+)/edit/$',                    lr(RhwEditView.as_view()),          name='rhw-edit'),
    url(r'^rhws/(?P<slug>[^/]+)/nominate/$',                lr(RhwNominateView.as_view()),      name='rhw-nominate'),
    url(r'^rhws/(?P<slug>[^/]+)/nominate/new$',             lr(RhwNominateNewView.as_view()),   name='rhw-nominate-new'),
    url(r'^rhws/(?P<rhw>[^/]+)/select/(?P<idea>[^/]+)/$',   pr('')(RhwSelectView.as_view()),    name='rhw-select'),

    url(r'^auth/password_reset/$', 'django.contrib.auth.views.password_reset', {
        'password_reset_form':  PasswordResetForm,
        'from_email':           settings.SERVER_EMAIL,
    }, name='password_reset'),
    url(r'^auth/',      include('django.contrib.auth.urls')),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^ckeditor/',  include('ckeditor_uploader.urls')),
]
