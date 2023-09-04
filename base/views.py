from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def cadastro(request):
    pass