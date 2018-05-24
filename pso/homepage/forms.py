from django.contrib.auth.models import User
from django import forms
from questionpage.models import Question

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
