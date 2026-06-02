from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import (
    Certificado,
    EmpresaProfissional,
    ExperienciaProfissional,
    Projeto,
    PublicacaoEstudo,
    Tag,
    TemaEstudo,
)


class PortfolioHomeTests(TestCase):
    def test_home_renders_empty_state(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Estágio em TI')
        self.assertContains(response, 'Análise de Dados')
        self.assertContains(response, 'og:title')
        self.assertContains(response, 'Nenhum projeto cadastrado ainda.')
        self.assertContains(response, 'Nenhuma ideia cadastrada ainda.')
        self.assertContains(response, 'Nenhum certificado cadastrado ainda.')
        self.assertContains(response, 'Nenhum tema de estudo cadastrado ainda.')

    def test_home_groups_projects_and_orders_certificates(self):
        tag = Tag.objects.create(nome='Django')
        projeto_real = Projeto.objects.create(
            nome='Projeto Real',
            descricao='Projeto publicado.',
            problema_resolvido='Organizar informacoes do portfolio.',
            aprendizado_obtido='Pratica com Django Admin e templates.',
            proximos_passos='Melhorar registros de dados.',
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
        empresa = EmpresaProfissional.objects.create(
            nome='Empresa Teste',
            cargo='Auxiliar Administrativo',
            periodo='2024 - 2025',
            descricao_curta='Experiencia com atendimento, sistemas e organizacao.',
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, projeto_real.nome)
        self.assertContains(response, 'Organizar informacoes do portfolio.')
        self.assertContains(response, 'Pratica com Django Admin e templates.')
        self.assertContains(response, 'Melhorar registros de dados.')
        self.assertContains(response, 'Projeto Futuro')
        self.assertContains(response, tag.nome)
        self.assertEqual(
            list(response.context['certificados']),
            [certificado_recente, certificado_antigo],
        )
        self.assertEqual(list(response.context['temas_estudo']), [tema_ativo])
        self.assertEqual(list(response.context['empresas_profissionais']), [empresa])
        self.assertContains(response, 'Excel')
        self.assertContains(response, 'Empresa Teste')
        self.assertNotContains(response, 'Tema Inativo')

    def test_sobre_page_renders_professional_positioning(self):
        response = self.client.get(reverse('sobre'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sobre Lucas Alves')
        self.assertContains(response, 'busco um estágio em TI')
        self.assertContains(response, 'Em aprendizado')
        self.assertContains(response, 'Experiencia real')


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


class AprendizadosProfissionaisTests(TestCase):
    def test_empresa_detail_lists_only_published_experiences(self):
        empresa = EmpresaProfissional.objects.create(
            nome='Cemtrabi',
            cargo='Suporte e atendimento',
            periodo='2024 - atual',
            descricao_curta='Contato com sistemas, atendimento e processos.',
        )
        publicado = ExperienciaProfissional.objects.create(
            empresa=empresa,
            titulo='Rotina de suporte',
            resumo='Aprendizado com atendimento, sistemas e organizacao.',
            atividades_realizadas='Atendimento, apoio em sistemas e organizacao de informacoes.',
            aprendizados_obtidos='Comunicar problemas com clareza e registrar informacoes.',
            habilidades_desenvolvidas='Atencao aos detalhes, suporte e organizacao.',
            ferramentas_competencias='Excel, Sistemas, Atendimento',
            status='publicado',
        )
        ExperienciaProfissional.objects.create(
            empresa=empresa,
            titulo='Rascunho profissional',
            resumo='Ainda nao publicado.',
            atividades_realizadas='Rascunho.',
            aprendizados_obtidos='Rascunho.',
            status='rascunho',
        )

        response = self.client.get(empresa.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, empresa.nome)
        self.assertContains(response, publicado.titulo)
        self.assertContains(response, 'Excel')
        self.assertNotContains(response, 'Rascunho profissional')


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
        empresa = EmpresaProfissional.objects.create(
            nome='Empresa',
            cargo='Atendimento',
            periodo='2024',
            descricao_curta='Experiencia profissional.',
        )
        experiencia = ExperienciaProfissional.objects.create(
            empresa=empresa,
            titulo='Aprendizado em processos',
            resumo='Resumo.',
            atividades_realizadas='Atividades.',
            aprendizados_obtidos='Aprendizados.',
        )

        self.assertEqual(str(projeto), 'Portfolio')
        self.assertEqual(str(certificado), 'Python')
        self.assertEqual(str(tema), 'Excel')
        self.assertEqual(str(publicacao), 'Tabela dinamica')
        self.assertEqual(str(empresa), 'Empresa')
        self.assertEqual(str(experiencia), 'Aprendizado em processos')
