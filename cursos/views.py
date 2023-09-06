from django.shortcuts import render
from cursos.forms import CursoForm

# Create your views here.
def criar_curso(request):
    form = CursoForm(request.POST or None)
    sucesso = False
    if form.is_valid():
        form.save()
        sucesso = True
    contexto = {
        'form': form,
        'sucesso': sucesso,
    }
    return render(request, 'criar_curso.html', contexto)