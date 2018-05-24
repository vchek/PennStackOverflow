from django.urls import path, re_path
from . import views

app_name = 'questionpage'

urlpatterns = [
    path('post/', views.PostQuestionView.as_view(), name='post_question'),
    re_path('^(?P<question_id>[0-9]+)/clear_notifications/$', views.clear_notification, name='clear_notification'),
    re_path('^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    re_path('^(?P<question_id>[0-9]+)/answer/$', views.PostAnswerView.as_view(), name='answer'),
    re_path('^(?P<question_id>[0-9]+)/answer/(?P<ans_id>[0-9]+)/comment$', views.post_comment, name='comment'),
    re_path('^(?P<question_id>[0-9]+)/answer/(?P<ans_id>[0-9]+)/comment/(?P<comment_id>[0-9]+)/delete$', views.delete_comment, name='delete_comment'),
    re_path('^(?P<pk>[0-9]+)/edit/$', views.QuestionUpdate.as_view(), name='edit_question'),
    re_path('^(?P<pk>[0-9]+)/delete/$', views.QuestionDelete.as_view(), name='delete_question'),
    re_path('^(?P<question_id>[0-9]+)/answer/(?P<pk>[0-9]+)/edit$', views.AnswerUpdate.as_view(), name='edit_answer'),
    re_path('^(?P<question_id>[0-9]+)/answer/(?P<pk>[0-9]+)/delete$', views.AnswerDelete.as_view(), name='delete_answer'),
    re_path('^vote/(?P<text_type>[a-z]+)/(?P<text_id>[0-9]+)/change=(?P<score_change>[+-]1)/$', views.vote, name='vote'),
]
