from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout, get_user
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from questionpage.models import Question, Notification, Answer
from .forms import UserForm
from functools import reduce
import json
import operator


def home(request):
    recent_question_pairs = []
    top_question_pairs = []
    alpha_question_pairs = []
    for q in Question.objects.all().order_by('date_posted'):
        length = len(Answer.objects.filter(question_answered=q.id))
        recent_question_pairs.append((q, length))
    for q in Question.objects.all().order_by('title')[:10]:
        length = len(Answer.objects.filter(question_answered=q.id))
        alpha_question_pairs.append((q, length))
    for q in Question.objects.all().order_by('score'):
        top_question_pairs.append((q, q.score))
    user = get_user(request)
    context = {
        'user': user,
        'recent_questions': recent_question_pairs,
        'top_questions': top_question_pairs,
        'alpha_questions': alpha_question_pairs,
        'all_notifications': [],
    }
    if not user.is_anonymous:
        notifications = Notification.objects.filter(user=get_user(request))
        context['all_notifications'] = notifications
    return render(request, 'homepage/home.html', context)


def logout(request):
    django_logout(request)
    return redirect('/')


def faq(request):
    context = {'user': request.user }
    return render(request, 'homepage/faq.html', context)


def contactus(request):
    context = {'user': request.user }
    return render(request, 'homepage/contactus.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'homepage/registration_form.html'

    def get (self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('/')
        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = UserForm
    template_name = 'homepage/login_form.html'

    def get (self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')

        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form})


class SearchListView(ListView):
    template_name = 'homepage/home.html'
    context_object_name = 'recent_questions'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query is not None:
            q_pairs = []
            if "[" in query and "]" in query:
                for q in self.get_tag_queryset(query):
                    q_pairs.append((q, len(Answer.objects.filter(question_answered=q.id))))
                return q_pairs
            else:
                for q in self.get_search_queryset(query):
                    q_pairs.append((q, len(Answer.objects.filter(question_answered=q.id))))
                return q_pairs

    def get_search_queryset(self, query):
        qs = query.split() or ['']
        mask1 = reduce(operator.and_, (Q(title__icontains=q) for q in qs))
        mask2 = reduce(operator.and_, (Q(body__icontains=q) for q in qs))
        return Question.objects.filter(mask1 | mask2)

    def get_tag_queryset(self, query):
        tags = query.split() or ['']
        tags = [tag[1:-1] for tag in tags if self.is_valid_tag(tag)]
        if not tags: return []
        mask = reduce(operator.and_, (Q(tags__icontains=tag) for tag in tags))
        return Question.objects.filter(mask)

    def is_valid_tag(self, tag):
        if len(tag) <3 or tag[0] != "[" or tag[-1] != "]": return False
        else: return tag[1:-1].isalnum()


def autocomplete(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        questions = Question.objects.filter(title__icontains=query)[:20]
        results = []
        for q in questions:
            results.append({'id': q.pk, 'label': q.title, 'value': q.title})
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
