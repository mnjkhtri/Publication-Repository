from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.models import ModelForm
from .import models


class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'slug', 'thumb']


class BiptexForm(forms.Form):
    bibtex = forms.FileField()
