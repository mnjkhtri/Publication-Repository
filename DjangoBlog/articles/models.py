from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
#A model for journal Article
class Article(models.Model): #this is like a table with fields
    title = models.CharField(max_length=100)
    slug=models.SlugField()
    co_authors =models.CharField(max_length=200,help_text="enter coauthors seperated by commas", default=None)
    pub_date=models.DateField(blank=True,default=None)
    journal =models.CharField(max_length=100,blank=True)
    volume=models.IntegerField(default=0)
    issue =models.IntegerField(default=0)
    pages =models.CharField(max_length=50,help_text="must be in form 333-444",blank=True)
    description =models.TextField(default="No description")

    author=models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING)
    citations =models.IntegerField(default=0)
    publisher =models.CharField(default=None,max_length=100)
    article_link =models.URLField(default=None)

    #auto add slug before save
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def getAuthors(self):
        return self.author.first_name+' '+self.author.last_name+','+self.co_authors

    def __str__(self): #whenever string version of the instance of this class is demanded, it will return the title
        return self.title
    
    def snippet(self):
        return self.body[:50]+'...'
    
   