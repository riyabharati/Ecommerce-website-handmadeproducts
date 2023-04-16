from django import forms
from .models import Profile
from django.forms import ModelForm

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','username']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)