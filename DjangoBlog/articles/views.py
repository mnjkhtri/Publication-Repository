
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from .models import Article
from django.contrib.auth.decorators import login_required
from .import forms

import bibtexparser

# import for pdf export--------------------
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from io import BytesIO


from django.template.loader import get_template

from xhtml2pdf import pisa


#pdf export here-------------------------
def create_pdf(request):
    articles=Article.objects.all()

    template_path = 'pdf_template.html'

    context = {'articles': articles}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="result.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
#export ends-------------------------

def biptexParser(f):
    bib_database = bibtexparser.load(f)
    return bib_database.entries[0]  # returns dict


def article_list(request):
    articles = Article.objects.all().order_by('pub_date')
    return render(request, 'articleslist.html', {'articles': articles})


@login_required(login_url='accounts:login')
def article_create(request, type):
    '''
        all form types are handled here
        form identified according to type parameter of url
        type= journal: it specifies the journal form is requested

    '''
    # work pending to do--------
    # migration of newly created models
    # handling different forms for different models
    # load different data from biptex
    biptexForm = forms.BiptexForm()
    print("type is :"+type)
    if type == 'journal':
        print("yes it is journal")
        form = forms.CreateArticle()

    elif type == 'conference':
        form = forms.CreateConference()

    elif type == 'Book':
        form = forms.CreateBook()

    if request.method == 'POST':
        print("Post request")
        if "bibtexUpload" in request.POST:

            print("got biptex")
            biptexForm = forms.BiptexForm(request.POST, request.FILES)
            if biptexForm.is_valid():
                file_handler = request.FILES['bibtex']
                result = biptexParser(file_handler)
                print(result)
                #common fields to all publishings
                data = {'title': result.get("title",""),
                    "co_authors":result.get("author",""),
                    "pages":result.get("pages","") }
                #coauthor also contains author name , need to work on this
                #non common fields parsed here
                
                data['journal']=result.get("journal","")
                data['publisher']=result.get("publisher","")
                data['volume']=result.get("volume","")
                data['pages']=result.get("pages","")
                    


                if type == 'journal':
                    print("yes it is journal")
                    form = forms.CreateArticle(initial=data)

                elif type == 'conference':
                    form = forms.CreateConference(initial=data)
                elif type == 'Book':
                    form = forms.CreateBook(initial=data)
        else:
            if type == 'journal':
                print("yes it is journal")
                form = forms.CreateArticle(request.POST)

            elif type == 'conference':
                form = forms.CreateConference(request.POST)
            elif type == 'Book':
                form = forms.CreateBook(request.POST)
            # form = forms.CreateArticle(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                return redirect('article:list')

    return render(request, 'article_create.html', {'form': form,
                                                   "biptex": biptexForm,
                                                   'type':type})


def article_detail(request, slug):
    # return HttpResponse(slug)
   # form = forms.CreateArticle()
    article = Article.objects.get(slug=slug)
    return render(request, 'article_obj.html', {'article': article})
