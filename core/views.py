from django.shortcuts import get_object_or_404, render

from .models import (
    Certificado,
    EmpresaProfissional,
    Projeto,
    PublicacaoEstudo,
    TemaEstudo,
)

def home(request):
    projetos = Projeto.objects.filter(tipo='real').prefetch_related('tags').order_by('-criado_em')
    futuros = Projeto.objects.filter(tipo='futuro').order_by('-criado_em')
    certificados = Certificado.objects.order_by('-data', 'nome')
    temas_estudo = TemaEstudo.objects.filter(ativo=True).order_by('ordem', 'titulo')
    empresas_profissionais = EmpresaProfissional.objects.order_by('ordem', '-criado_em', 'nome')

    return render(request, 'core/home.html', {
        'projetos': projetos,
        'futuros': futuros,
        'certificados': certificados,
        'temas_estudo': temas_estudo,
        'empresas_profissionais': empresas_profissionais,
    })


def sobre(request):
    return render(request, 'core/sobre_detail.html')


def tema_estudo_detail(request, slug):
    tema = get_object_or_404(TemaEstudo, slug=slug, ativo=True)
    publicacoes = tema.publicacoes.filter(status='publicado').order_by('-criado_em')

    return render(request, 'core/tema_estudo_detail.html', {
        'tema': tema,
        'publicacoes': publicacoes,
    })


def publicacao_estudo_detail(request, tema_slug, slug):
    publicacao = get_object_or_404(
        PublicacaoEstudo.objects.select_related('tema').prefetch_related('imagens_extras'),
        tema__slug=tema_slug,
        tema__ativo=True,
        slug=slug,
        status='publicado',
    )

    return render(request, 'core/publicacao_estudo_detail.html', {
        'publicacao': publicacao,
        'tema': publicacao.tema,
    })


def empresa_profissional_detail(request, slug):
    empresa = get_object_or_404(EmpresaProfissional, slug=slug)
    experiencias = empresa.experiencias.filter(status='publicado').prefetch_related('imagens').order_by('-criado_em')

    return render(request, 'core/empresa_profissional_detail.html', {
        'empresa': empresa,
        'experiencias': experiencias,
    })
