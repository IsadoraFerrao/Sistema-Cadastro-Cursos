from django.shortcuts import render
from django.http import HttpResponse 
from base.forms import CadastroForm
from base.models import Cadastro
# Register your models here.

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def cadastro(request):
    sucesso = False
    if request.method == 'GET':
        form = CadastroForm()
    else:
        form = CadastroForm(request.POST)
        if form.is_valid():
            sucesso = True
            form.save()
    contexto = {
        'form': form,
        'sucesso': sucesso
    }
    return render(request, 'cadastro.html', contexto)
