from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import widgets
from django.forms.models import ModelForm
from .import models


class DateInput(forms.DateInput):
    input_type = 'date'

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields ='__all__'
        exclude =['slug','author']
        widgets={
            "pub_date": DateInput()
        }

class CreateBook(forms.ModelForm):
    class Meta:
        model = models.Book
        fields ='__all__'
        exclude =['slug','author']
        widgets={
            "pub_date": DateInput()
        }

class CreateConference(forms.ModelForm):
    class Meta:
        model = models.ConferenceArticle
        fields ='__all__'
        exclude =['slug','author']
        widgets={
            "pub_date": DateInput(),
        }



class BiptexForm(forms.Form):
    bibtex_form = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
