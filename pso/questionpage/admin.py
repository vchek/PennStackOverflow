from django.contrib import admin

from .models import Question, Answer, Comment, Vote, Notification

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Notification)
