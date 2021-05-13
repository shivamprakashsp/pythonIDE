from django.forms import fields
from .models import Snippet
from django import forms
from django_ace import AceWidget


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
      
        fields = ["filename","text",'input','output']
