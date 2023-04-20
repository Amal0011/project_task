from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from todo_app.models import Task

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields = ['task_name']

class PasswordResetForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(label = 'password1',widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label = 'password2',widget=forms.PasswordInput(attrs={"class":"form-control"}))
         