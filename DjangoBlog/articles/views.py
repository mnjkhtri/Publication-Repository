
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Article
from django.contrib.auth.decorators import login_required
from .import forms

import bibtexparser
# Create your views here.


def biptexParser(f):
    bib_database = bibtexparser.load(f)
    return bib_database.entries[0] #returns dict


def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, 'articleslist.htm', {'articles': articles})


@login_required(login_url='accounts:login')
def article_create(request):
    biptexForm = forms.BiptexForm()
    form = forms.CreateArticle()
    if request.method == 'POST':
        print(request.POST)
        if "bibtexUpload" in request.POST:
            print("got biptex")
            biptexForm = forms.BiptexForm(request.POST, request.FILES)
            if biptexForm.is_valid():
                file_handler = request.FILES['bibtex']
                result =biptexParser(file_handler)
                print(result["title"])
                #we need to provide initials for form in data below
                
                data = { 'title': result['title'],}
                form =forms.CreateArticle(initial=data)
        else:
            form = forms.CreateArticle(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                return redirect('article:list')

    return render(request, 'article_create.html', {'form': form,
                                                   "biptex": biptexForm})


def article_detail(request, slug):
    # return HttpResponse(slug)
   # form = forms.CreateArticle()
    article = Article.objects.get(slug=slug)
    return render(request, 'article_obj.htm', {'article': article})
