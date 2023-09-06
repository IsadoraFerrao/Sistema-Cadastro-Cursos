from django.shortcuts import render
from cursos.forms import CursoForm
from django.views.decorators.cache import cache_page
from cursos.models import Curso

# Create your views here.
@cache_page(30)
def criar_curso(request):
    cursos = Curso.objects.all()
    form = CursoForm(request.POST or None)
    sucesso = False
    if form.is_valid():
        form.save()
        sucesso = True
    contexto = {
        'form': form,
        'sucesso': sucesso,
        'cursos': cursos,
    }
    return render(request, 'criar_curso.html', contexto)