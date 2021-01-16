from django.forms import ModelForm
from .models import MakePost
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MakePostForm(ModelForm):

    class Meta:
        model = MakePost
        fields = ("title", "content", "photo")

class UserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Username', max_length=16)
    email = forms.EmailField(required=False, label='Email', help_text='(Optional)')
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label='Password confirmation', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
