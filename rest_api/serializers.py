from rest_framework.serializers import ModelSerializer
from cursos.models import Curso

class CursoModelSerializer(ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
