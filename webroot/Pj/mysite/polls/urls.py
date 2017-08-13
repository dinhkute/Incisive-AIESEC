from django.conf.urls import url
from . import views
from django.contrib.auth.views import (login, logout,
                                       password_reset,
                                       password_reset_complete,
                                       password_reset_done,
                                        password_reset_confirm)

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'login/$', login, {'template_name':'polls/login.html'}, name = 'login'),
    url(r'logout/$', logout, {'template_name':'polls/logout.html'}, name='logout'),
    url(r'register/$', views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='changepassword'),
    url(r'^reset-password/$', password_reset,
        {'template_name': 'polls/reset_password.html', 'post_reset_redirect': 'polls:password_reset_done',
         'email_template_name': 'polls/reset_password_email.html'}, name='reset_password'),

    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'polls/reset_password_done.html'},
        name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'polls/reset_password_confirm.html',
         'post_reset_redirect': 'polls:password_reset_complete'}, name='password_reset_confirm'),

    url(r'^reset-password/complete/$', password_reset_complete,
        {'template_name': 'polls/reset_password_complete.html'}, name='password_reset_complete'),
    url(r'^test/$', views.testTemplate.as_view(), name='test'),
    url(r'^test/(?P<pk>[0-9]+)/$', views.DetailForm, name='detailform'),
    url(r'^listform/$', views.RegisterFormList.as_view(), name='listform'),
    url(r'^listform/(?P<pk>[0-9]+)/$', views.AnswerForm, name='question'),
    url(r'^event/$', views.Event.as_view(), name='event'),
    url(r'^event/(?P<pk>[0-9]+)/$', views.DetailedEvent, name='detail_event'),
    url(r'^(?P<event_id>[0-9]+)/registerevent/$', views.UserEvent, name='register_event'),
]