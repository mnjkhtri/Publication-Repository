from django import forms
from django.forms.models import ModelForm
from .import models

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields=['title','body','slug','thumb']
        


