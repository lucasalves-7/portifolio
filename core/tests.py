from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Certificado, Projeto, PublicacaoEstudo, Tag, TemaEstudo


class PortfolioHomeTests(TestCase):
    def test_home_renders_empty_state(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum projeto cadastrado ainda.')
        self.assertContains(response, 'Nenhuma ideia cadastrada ainda.')
        self.assertContains(response, 'Nenhum certificado cadastrado ainda.')
        self.assertContains(response, 'Nenhum tema de estudo cadastrado ainda.')

    def test_home_groups_projects_and_orders_certificates(self):
        tag = Tag.objects.create(nome='Django')
        projeto_real = Projeto.objects.create(
            nome='Projeto Real',
            descricao='Projeto publicado.',
            tipo='real',
        )
        projeto_real.tags.add(tag)
        Projeto.objects.create(
            nome='Projeto Futuro',
            descricao='Ideia em planejamento.',
            tipo='futuro',
        )
        certificado_recente = Certificado.objects.create(
            nome='Certificado Recente',
            instituicao='Escola',
            data=date(2026, 4, 1),
        )
        certificado_antigo = Certificado.objects.create(
            nome='Certificado Antigo',
            instituicao='Escola',
            data=date(2025, 4, 1),
        )
        tema_ativo = TemaEstudo.objects.create(
            titulo='Excel',
            descricao_curta='Estudos de planilhas e dados.',
            ordem=1,
        )
        TemaEstudo.objects.create(
            titulo='Tema Inativo',
            descricao_curta='Nao deve aparecer.',
            ativo=False,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, projeto_real.nome)
        self.assertContains(response, 'Projeto Futuro')
        self.assertContains(response, tag.nome)
        self.assertEqual(
            list(response.context['certificados']),
            [certificado_recente, certificado_antigo],
        )
        self.assertEqual(list(response.context['temas_estudo']), [tema_ativo])
        self.assertContains(response, 'Excel')
        self.assertNotContains(response, 'Tema Inativo')


class LabEstudosTests(TestCase):
    def test_tema_detail_lists_only_published_posts(self):
        tema = TemaEstudo.objects.create(
            titulo='SQL',
            descricao_curta='Consultas e organizacao de dados.',
        )
        publicado = PublicacaoEstudo.objects.create(
            tema=tema,
            titulo='Primeiras consultas',
            resumo='Aprendizado com SELECT e filtros.',
            conteudo='Conteudo completo do estudo.',
            tecnologias_utilizadas='SQL, SQLite',
            status='publicado',
        )
        PublicacaoEstudo.objects.create(
            tema=tema,
            titulo='Rascunho interno',
            resumo='Ainda nao publicado.',
            conteudo='Conteudo em rascunho.',
            status='rascunho',
        )

        response = self.client.get(tema.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tema.titulo)
        self.assertContains(response, publicado.titulo)
        self.assertNotContains(response, 'Rascunho interno')

    def test_publicacao_detail_requires_published_status(self):
        tema = TemaEstudo.objects.create(
            titulo='Power BI',
            descricao_curta='Dashboards em aprendizado.',
        )
        publicacao = PublicacaoEstudo.objects.create(
            tema=tema,
            titulo='Dashboard inicial',
            resumo='Resumo do estudo.',
            conteudo='Conteudo completo.',
            tecnologias_utilizadas='Power BI, Excel',
            aprendizados_principais='Organizar dados antes do visual.',
            dificuldades_encontradas='Escolher os indicadores.',
            solucao_aplicada='Separar medidas e dimensoes.',
            video_url='https://youtu.be/abc123',
            status='publicado',
        )
        rascunho = PublicacaoEstudo.objects.create(
            tema=tema,
            titulo='Post privado',
            resumo='Resumo privado.',
            conteudo='Conteudo privado.',
            status='rascunho',
        )

        response = self.client.get(publicacao.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, publicacao.titulo)
        self.assertContains(response, 'https://www.youtube.com/embed/abc123')
        self.assertContains(response, 'Power BI')
        self.assertEqual(self.client.get(rascunho.get_absolute_url()).status_code, 404)


class ModelStringTests(TestCase):
    def test_model_string_representations(self):
        projeto = Projeto.objects.create(nome='Portfolio', descricao='Site pessoal.')
        certificado = Certificado.objects.create(
            nome='Python',
            instituicao='Curso',
            data=date(2026, 1, 1),
        )
        tema = TemaEstudo.objects.create(
            titulo='Excel',
            descricao_curta='Planilhas e dados.',
        )
        publicacao = PublicacaoEstudo.objects.create(
            tema=tema,
            titulo='Tabela dinamica',
            resumo='Resumo.',
            conteudo='Conteudo.',
        )

        self.assertEqual(str(projeto), 'Portfolio')
        self.assertEqual(str(certificado), 'Python')
        self.assertEqual(str(tema), 'Excel')
        self.assertEqual(str(publicacao), 'Tabela dinamica')
