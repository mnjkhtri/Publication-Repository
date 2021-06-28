from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model): #this is like a table with fields
    title = models.CharField(max_length=100)
    slug=models.SlugField()
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    thumb=models.ImageField(default="default.jpg",blank=True)
    author=models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING)

    def __str__(self): #whenever string version of the instance of this class is demanded, it will return the title
        return self.title
    
    def snippet(self):
        return self.body[:50]+'...'
    
   