from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    tags = models.CharField(max_length=200, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def tags_as_list(self):
        return self.tags.split(',')

class Answer(models.Model):
    list_display=('id',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_posted = models.DateTimeField(default=timezone.now)
    body = models.TextField(blank=False)
    question_answered = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.pk)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_posted = models.DateTimeField(default=timezone.now, blank=False)
    body = models.TextField()
    answer_commented = models.ForeignKey(Answer, related_name = 'comments', on_delete=models.CASCADE, default=None)
    score = models.IntegerField(default=0)

    def __str__(self):
        return (str(self.author) + "'s' Comment")

## TODO: Return to this idea -- make sure users can't upvote or downvote multiple times

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False) ##TODO: Check this -- does this make sense?
    text_id = models.PositiveIntegerField()
    is_upvoted = models.IntegerField()
    text_type = models.TextField()

    def check_if_upvoted(self):
        return self.is_upvoted

    def __str__(self):
        return (str(self.user) + "'s' Vote")


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False)

    def __str__(self):
        strng = "Someone answered your question '{}...'"
        return (strng.format(self.question.title[:40]))
