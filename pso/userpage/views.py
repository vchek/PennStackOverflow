from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from questionpage.models import Question, Answer, Comment
from django.http import HttpResponse
from .fusioncharts import FusionCharts


def change_password(request, username):
    if (request.user.username == username):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return profile(request, username)
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'userpage/change_password.html', {
            'form': form
        })
    else:
        return redirect('/')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    questions = Question.objects.filter(author=user).order_by('date_posted')
    answers = Answer.objects.filter(author=user).order_by('date_posted')
    context = dict(user=user, questions=questions, answers=answers, viewer=request.user)
    return render(request, 'userpage/profile.html', context)


def graph(request, username):
    user = get_object_or_404(User, username=username)
    questions = Question.objects.filter(author=user).order_by('date_posted')
    answers = Answer.objects.filter(author=user).order_by('date_posted')
    comments = Comment.objects.filter(author=user).order_by('date_posted')

    column2d = FusionCharts("column2d", "ex1" , "600", "400", "chart-1", "json",
          # The data is passed as a string in the `dataSource` as parameter.
      """{
            "chart":{
              "caption":"%s\'s Contributions",
              "subCaption":"Contributions to Penn Stack Overflow",
              "numberPrefix":"",
              "theme":"ocean"
            },
            "data":[
              {"label":"Questions", "value":"%s"},
              {"label":"Answers", "value":"%s"},
              {"label":"Comments", "value":"%s"},
            ]
        }""" % (username, len(questions), len(answers), len(comments)))
    return render(request, 'userpage/graph.html', {'output' : column2d.render()})

def change_picture(request, username):
    if (request.user.username == username):
        if request.method == 'POST':
            user = User.objects.get(username=username)
            img = request.FILES["mypicture"]
            user.profile.picture = img
            user.profile.save()
            return redirect('.')
        else:
            return render(request, 'userpage/change_picture.html')
    else:
        return redirect('/')
