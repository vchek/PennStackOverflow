from django.shortcuts import render, get_object_or_404, redirect
from questionpage.models import Question, Answer, Comment, Vote, Notification
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AnswerForm, QuestionForm
from django.template.defaulttags import register
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout as django_logout
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
import bleach, re
import sys


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = list(Answer.objects.filter(question_answered__id=question_id).order_by('-score'))
    context = {'question': question, 'user': request.user, 'answers': answers}
    return render(request, 'questionpage/index.html', context)


def clear_notification(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    notifications = Notification.objects.filter(question=question).delete()
    return detail(request, question_id)


def vote(request, text_id, score_change, text_type):
    score_change = int(score_change)

    if (text_type == 'question'):
        return_id = text_id
        voted = get_object_or_404(Question, pk=text_id)
    elif (text_type == 'answer'):
        return_id = get_object_or_404(Answer, pk=text_id).question_answered.id
        voted = get_object_or_404(Answer, pk=text_id)
    else:
        return_id = get_object_or_404(Comment, pk=text_id).answer_commented.question_answered.id
        voted = get_object_or_404(Comment, pk=text_id)

    if request.user.is_authenticated:
        if vote_already_exists(user=request.user, text_id=text_id, text_type=text_type, is_upvoted=score_change):
            score_change = 0
        elif vote_is_being_switched(user=request.user, text_id=text_id, text_type=text_type, is_upvoted=score_change):
            Vote.objects.get(user=request.user, text_id=text_id, text_type=text_type, is_upvoted=(score_change*-1)).delete()
            new_vote = Vote(user=request.user, text_id=text_id, text_type=text_type, is_upvoted=score_change)
            new_vote.save()
            score_change *= 2 # need to increment by + or - 2 to overcome original vote
        else:
            new_vote = Vote(user=request.user, text_id=text_id, text_type=text_type, is_upvoted=score_change)
            new_vote.save()
    else:
        score_change = 0

    voted.score += score_change
    voted.save()
    return detail(request, return_id)


def vote_already_exists(user, text_id, text_type, is_upvoted):
    if Vote.objects.filter(user=user, text_id=text_id, text_type=text_type, is_upvoted=is_upvoted).count() > 0:
        return True
    else:
        return False


def vote_is_being_switched(user, text_id, text_type, is_upvoted):
    if Vote.objects.filter(user=user, text_id=text_id, text_type=text_type).count() > 0:
        return True
    else:
        return False


def post_comment(request, question_id, ans_id):
    answer = get_object_or_404(Answer, pk=ans_id)
    Comment(author=request.user, body=request.POST.get("text"), answer_commented=answer).save()
    return HttpResponseRedirect('../..')


def delete_comment(request, question_id, ans_id, comment_id):
    return_id = get_object_or_404(Comment, pk=comment_id).answer_commented.question_answered.id
    Comment.objects.filter(id=comment_id).delete()
    to_link = '/questions/%s/' % (question_id)
    return HttpResponseRedirect(redirect_to=to_link)


class AnswerUpdate(UpdateView):
    model = Answer
    fields = ['body']
    template_name = 'questionpage/answer_question_form.html'
    success_url = '../..'


class AnswerDelete(DeleteView):
    model = Answer
    fields = ['body']
    template_name = 'questionpage/delete_form.html'
    success_url = '../..'


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['title', 'body', 'tags']
    template_name = 'questionpage/edit_question_form.html'
    success_url = '..'


class QuestionDelete(DeleteView):
    model = Question
    fields = ['title', 'body', 'tags']
    template_name = 'questionpage/delete_form.html'
    def get_success_url(self):
        return reverse_lazy('homepage:home')


def add_question_hyperlinks(text):
    new_text = text
    matches = re.findall(r'(@[0-9]+)', new_text)
    for at_q in matches:
        q_num = at_q[1:]
        link = '<a href="http://127.0.0.1:8000/questions/' + q_num + '/">' + at_q + "</a>"
        new_text = re.sub(at_q, link, new_text)
    return new_text


class PostQuestionView(LoginRequiredMixin, View):
    form_class = QuestionForm
    template_name = 'questionpage/post_question_form.html'
    login_url = '/login/'
    redirect_field_name = ''

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        author = request.user
        title = request.POST['title']
        title = bleach.clean(title, tags = ['b', 'a'],)
        body = request.POST['body']
        body = add_question_hyperlinks(body)
        body = bleach.clean(body, tags = ['b', 'a'],)
        tags = self.clean_tags(request.POST['tags'])
        Question(author=author, title=title, body=body, tags=tags).save()
        print(request.path)
        return HttpResponseRedirect('/')

    def clean_tags(self, tags):
        tag_lst = [tag.strip() for tag in tags.split(",")]
        tag_lst = [tag for tag in tag_lst if tag and tag.isalnum()]
        tags = ",".join(tag_lst)
        return tags


class PostAnswerView(LoginRequiredMixin, View):
    form_class = AnswerForm
    template_name = 'questionpage/answer_question_form.html'
    login_url = '/login/'

    def get(self, request, question_id):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, question_id):
        body = request.POST['body']
        body = add_question_hyperlinks(body)
        body = bleach.clean(body, tags=['b', 'a'], )
        question = get_object_or_404(Question, pk=question_id)
        answer = Answer(author=request.user, body=body, question_answered=question)
        answer.save()
        create_notification(question.author, question, answer)
        return HttpResponseRedirect('..')


def create_notification(user, question, answer):
    if not Notification.objects.filter(question=question).exists():
        notification = Notification(user=user, question=question, answer=answer)
        notification.save()
