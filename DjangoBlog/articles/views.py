
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from .models import Article
from django.contrib.auth.decorators import login_required
from .import forms

import bibtexparser

#import for pdf export--------------------
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def html_to_pdf_view(request):
    articles =Article.objects.all().order_by('-date')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    textobject = p.beginText()
    textobject.setTextOrigin(inch, 2.5*inch)
    
    for article in articles:
        textobject.setFont("Helvetica-Bold", 25)
        textobject.textLine(article.title)
        textobject.setFont("Helvetica", 14)
        textobject.textLine(article.body)
    p.drawText(textobject)
    # x = 0.5*inch
    # y = 2.7*inch
    # for article in articles:
    #     p.setFont("Helvetica-Bold", 30)
    #     p.drawString(x,y,article.title)
    #     y = y-33
    #     p.setFont("Helvetica", 20)
    #     p.drawString(x,y,article.body)
    #     y = y-22
    # Start writing the PDF here
    # for article in articles:
    #     p.setFont("Helvetica-Bold",30,leading=10)
    #     p.drawString(0, y,article.title+'\n')
    #     y=y-20
    #     p.setFont("Helvetica",20,leading=10)
    #     p.drawString(0,y,article.body+'\n')
    #     y=y-40
        
    # End writing

    p.showPage()
    p.save()
    buffer.seek(0)

    # pdf = buffer.getvalue()
    # buffer.close()
    # response.write(pdf)

    return FileResponse(buffer, as_attachment=False,filename="mypage.pdf")
#-------------pdf export ends here-----------------------------------------------

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
