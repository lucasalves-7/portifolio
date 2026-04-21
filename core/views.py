from django.shortcuts import render
from .models import Certificado, Projeto

def home(request):
    projetos = Projeto.objects.filter(tipo='real')
    futuros = Projeto.objects.filter(tipo='futuro')
    certificados = Certificado.objects.all()

    return render(request, 'core/home.html', {
        'projetos': projetos,
        'futuros': futuros,
        'certificados': certificados,
    })