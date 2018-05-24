from django.contrib.auth.models import User
from django import forms
from questionpage.models import Question, Answer


class AnswerForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        fields = ['body']

class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    body = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=200)

    class Meta:
        model = Question
        fields = ['title', 'body', 'tags']
