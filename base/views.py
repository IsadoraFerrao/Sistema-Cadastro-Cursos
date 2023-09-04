from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def cadastro(request):
    return render(request, 'cadastro.html')
