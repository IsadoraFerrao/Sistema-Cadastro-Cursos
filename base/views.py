from django.shortcuts import render
from django.http import HttpResponse 
from base.forms import CadastroForm

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')


def cadastro(request):
    sucesso = False   
    form = CadastroForm(request.POST or None)
    if form.is_valid(): 
        sucesso = True
        form.save()
    contexto = {
        'form':form,
        'sucesso': sucesso
    }
    return render(request, 'cadastro.html', contexto)


