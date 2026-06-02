from datetime import date

from django.core.management.base import BaseCommand

from core.models import (
    Certificado,
    EmpresaProfissional,
    ExperienciaProfissional,
    Projeto,
    PublicacaoEstudo,
    Tag,
    TemaEstudo,
)


class Command(BaseCommand):
    help = "Cria dados iniciais de exemplo para o portfolio."

    def handle(self, *args, **options):
        dados_tag, _ = Tag.objects.get_or_create(nome="Dados")
        django_tag, _ = Tag.objects.get_or_create(nome="Django")
        suporte_tag, _ = Tag.objects.get_or_create(nome="Suporte TI")

        projeto, _ = Projeto.objects.get_or_create(
            nome="Portfolio Lucas Alves Tech",
            defaults={
                "descricao": "Portfolio dinamico para apresentar estudos, projetos e aprendizados profissionais.",
                "problema_resolvido": "Organizar em um unico lugar a evolucao em TI, dados, desenvolvimento e suporte.",
                "aprendizado_obtido": "Pratica com Django, templates, admin, uploads, SEO e deploy.",
                "proximos_passos": "Cadastrar mais publicacoes reais no Lab de Estudos e evoluir dashboards de dados.",
                "tipo": "real",
            },
        )
        projeto.tags.add(dados_tag, django_tag, suporte_tag)

        TemaEstudo.objects.get_or_create(
            titulo="Excel",
            defaults={
                "descricao_curta": "Estudos de planilhas, organizacao de dados, formulas e indicadores.",
                "ordem": 1,
            },
        )
        tema_sql, _ = TemaEstudo.objects.get_or_create(
            titulo="SQL",
            defaults={
                "descricao_curta": "Consultas, filtros, organizacao de tabelas e leitura de informacoes.",
                "ordem": 2,
            },
        )
        PublicacaoEstudo.objects.get_or_create(
            tema=tema_sql,
            titulo="Primeiras consultas com SQL",
            defaults={
                "resumo": "Registro de estudo sobre SELECT, filtros e organizacao de resultados.",
                "conteudo": "Neste estudo pratiquei consultas basicas, leitura de tabelas e filtros simples.",
                "tecnologias_utilizadas": "SQL, SQLite",
                "aprendizados_principais": "Entendi melhor como buscar informacoes e transformar dados em respostas.",
                "dificuldades_encontradas": "Organizar a logica antes de escrever a consulta.",
                "solucao_aplicada": "Separar o problema em partes menores e testar cada filtro.",
                "status": "publicado",
            },
        )

        empresa, _ = EmpresaProfissional.objects.get_or_create(
            nome="Experiencia profissional inicial",
            defaults={
                "cargo": "Atendimento, sistemas e organizacao",
                "periodo": "Atualize o periodo no Admin",
                "descricao_curta": "Base profissional ligada a atendimento, processos, sistemas, Excel e resolucao de problemas.",
                "ordem": 1,
            },
        )
        ExperienciaProfissional.objects.get_or_create(
            empresa=empresa,
            titulo="Aprendizados com atendimento e sistemas",
            defaults={
                "resumo": "Experiencia voltada para organizacao, comunicacao e apoio em rotinas com sistemas.",
                "atividades_realizadas": "Atendimento, consulta em sistemas, organizacao de informacoes e apoio a rotinas internas.",
                "aprendizados_obtidos": "Aprendi a registrar problemas com clareza, manter organizacao e buscar solucoes praticas.",
                "habilidades_desenvolvidas": "Comunicacao, atencao aos detalhes, Excel, atendimento e suporte basico.",
                "ferramentas_competencias": "Excel, Sistemas corporativos, Atendimento, Organizacao",
                "desafios_enfrentados": "Lidar com demandas diferentes mantendo prioridade e clareza.",
                "resultados_alcancados": "Maior seguranca para atuar em processos, suporte e organizacao de informacoes.",
                "status": "publicado",
            },
        )

        Certificado.objects.get_or_create(
            nome="Estudos em tecnologia",
            instituicao="Atualize a instituicao no Admin",
            data=date(2026, 1, 1),
        )

        self.stdout.write(self.style.SUCCESS("Dados iniciais criados ou atualizados com sucesso."))
