from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/invoice/$', views.invoice, name='invoice'),
    url(r'^(?P<question_id>[0-9]+)/vote/(?P<vote_id>[0-9]+)', views.vote, name='vote'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]
