from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
#A model for journal Article
class Article(models.Model): #this is like a table with fields
    title = models.CharField(max_length=100)
    slug=models.SlugField()
    co_authors =models.CharField(max_length=200,help_text="enter coauthors seperated by and", default=None)
    pub_date=models.DateField(blank=True,default=None)
    journal =models.CharField(max_length=100,blank=True)
    volume=models.IntegerField(default=0)
    issue =models.IntegerField(default=0)
    pages =models.CharField(max_length=50,help_text="must be in form nn--nn",blank=True)
    description =models.TextField(default="No description")

    author=models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING,related_name="journals")
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

    def getApaAuthors(self):
        new_list = self.co_authors.split(' and')
        print(new_list)
        result = ''
        #need to generate user list in apa format
        for item in new_list:
            if item ==new_list[-1]:
                #check if it is last element to append &
                print('yes')
                result +='& '
            temp=item.split()
            if len(temp)==3:
                result+= temp[0]+temp[1][0]+'.'+temp[2][0]+'.,'
            else:
                result+= temp[0]+temp[1][0]+'.,'
        
        return result

    def get_pub_year(self):
        return self.pub_date.year

    def __str__(self): #whenever string version of the instance of this class is demanded, it will return the title
        return self.title
    
    def snippet(self):
        return self.body[:50]+'...'
    
   
class Book(models.Model):
    title = models.CharField(max_length=100)
    slug=models.SlugField()
    co_authors =models.CharField(max_length=200,help_text="enter coauthors seperated by and", default=None)
    pub_date=models.DateField(blank=True,default=None)
    description =models.TextField(default="No description")
    author=models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING,related_name="books")
    co_authors =models.CharField(max_length=200,help_text="enter coauthors seperated by commas", default=None)


    edition = models.CharField(max_length=50, null=True, blank=True)
    isbn = models.CharField(max_length=50, null=True, blank=True)
    chapters = models.CharField(max_length=50, null=True, blank=True)
    book_link =models.URLField(default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def __str__(self): #whenever string version of the instance of this class is demanded, it will return the title
        return self.title

    def getAuthors(self):
        return self.author.first_name+' '+self.author.last_name+','+self.co_authors

    def getApaAuthors(self):
        new_list = self.co_authors.split(' and')
        print(new_list)
        result = ''
        #need to generate user list in apa format
        for item in new_list:
            if item ==new_list[-1]:
                #check if it is last element to append &
                print('yes')
                result +='& '
            temp=item.split()
            if len(temp)==3:
                result+= temp[0]+temp[1][0]+'.'+temp[2][0]+'.,'
            else:
                result+= temp[0]+temp[1][0]+'.,'
        
        return result
    
    
        


class ConferenceArticle(models.Model):
    title = models.CharField(max_length=100)
    slug=models.SlugField()
    co_authors =models.CharField(max_length=200,help_text="enter coauthors seperated by commas", default=None)
    pub_date=models.DateField(blank=True,default=None)
    description =models.TextField(default="No description")
    author=models.ForeignKey(User,default=None,on_delete=models.DO_NOTHING,related_name="conferenceArticle")
    co_authors =models.CharField(max_length=200,help_text="enter coauthors seperated by and", default=None)

    conference_name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    organised_date = models.DateField(
        null=True, blank=True)

    conference_link =models.URLField(blank=True,null=True ,default="http://nolink.com")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ConferenceArticle, self).save(*args, **kwargs)

    def __str__(self): #whenever string version of the instance of this class is demanded, it will return the title
        return self.title

    def getAuthors(self):
        return self.author.first_name+' '+self.author.last_name+','+self.co_authors

    def getApaAuthors(self):
        new_list = self.co_authors.split(' and')
        print(new_list)
        result = ''
        #need to generate user list in apa format
        for item in new_list:
            if item ==new_list[-1]:
                #check if it is last element to append &
                print('yes')
                result +='& '
            temp=item.split()
            if len(temp)==3:
                result+= temp[0]+temp[1][0]+'.'+temp[2][0]+'.,'
            else:
                result+= temp[0]+temp[1][0]+'.,'
        
        return result

    



