from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Certificado,
    EmpresaProfissional,
    ExperienciaProfissional,
    ImagemExperienciaProfissional,
    ImagemPublicacaoEstudo,
    Projeto,
    PublicacaoEstudo,
    Tag,
    TemaEstudo,
)


admin.site.site_header = "Lucas Admin"
admin.site.site_title = "Painel Administrativo"
admin.site.index_title = "Gestão do Portfólio"


@admin.register(Projeto)
class ProjetoAdmin(ModelAdmin):
    list_display = (
        "nome",
        "tipo",
        "tags_resumo",
        "link_disponivel",
        "imagem_disponivel",
        "criado_em",
    )
    list_filter = ("tipo", "tags", "criado_em")
    search_fields = (
        "nome",
        "descricao",
        "problema_resolvido",
        "aprendizado_obtido",
        "proximos_passos",
        "tags__nome",
    )
    ordering = ("-criado_em", "nome")
    date_hierarchy = "criado_em"
    list_per_page = 12
    autocomplete_fields = ("tags",)
    readonly_fields = ("criado_em", "preview_imagem")
    save_on_top = True
    fieldsets = (
        (
            "Informacoes principais",
            {
                "fields": ("nome", "descricao", "problema_resolvido", "aprendizado_obtido", "proximos_passos"),
                "description": "Dados centrais do projeto exibidos no portfolio.",
            },
        ),
        (
            "Classificacao e organizacao",
            {
                "fields": ("tipo", "tags"),
                "description": "Defina a categoria do projeto e associe tags para facilitar a busca.",
            },
        ),
        (
            "Midia e publicacao",
            {
                "fields": ("link", "imagem", "preview_imagem"),
                "description": "Adicione link externo e imagem de capa para melhorar a apresentacao.",
            },
        ),
        (
            "Registro",
            {
                "fields": ("criado_em",),
            },
        ),
    )
    @admin.display(description="Tags")
    def tags_resumo(self, obj):
        tags = list(obj.tags.values_list("nome", flat=True)[:3])
        if not tags:
            return "-"
        resumo = ", ".join(tags)
        if obj.tags.count() > 3:
            resumo += "..."
        return resumo

    @admin.display(description="Link", boolean=True)
    def link_disponivel(self, obj):
        return bool(obj.link)

    @admin.display(description="Imagem", boolean=True)
    def imagem_disponivel(self, obj):
        return bool(obj.imagem)

    @admin.display(description="Preview")
    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" alt="Preview de {}" style="max-height: 140px; border-radius: 12px;" />',
                obj.imagem.url,
                obj.nome,
            )
        return "Nenhuma imagem enviada."


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("nome", "total_projetos")
    search_fields = ("nome",)
    ordering = ("nome",)
    list_per_page = 20
    save_on_top = True
    fieldsets = (
        (
            "Identificacao da tag",
            {
                "fields": ("nome",),
                "description": "Use nomes curtos e objetivos para facilitar a classificacao dos projetos.",
            },
        ),
    )
    @admin.display(description="Projetos vinculados")
    def total_projetos(self, obj):
        return obj.projeto_set.count()


@admin.register(Certificado)
class CertificadoAdmin(ModelAdmin):
    list_display = (
        "nome",
        "instituicao",
        "data",
        "link_disponivel",
        "imagem_disponivel",
    )
    list_filter = ("instituicao", "data")
    search_fields = ("nome", "instituicao")
    ordering = ("-data", "nome")
    date_hierarchy = "data"
    list_per_page = 12
    readonly_fields = ("preview_imagem",)
    save_on_top = True
    fieldsets = (
        (
            "Dados do certificado",
            {
                "fields": ("nome", "instituicao", "data"),
                "description": "Informacoes principais para identificar e organizar o certificado.",
            },
        ),
        (
            "Comprovacao e midia",
            {
                "fields": ("link", "imagem", "preview_imagem"),
                "description": "Inclua o link do certificado e uma imagem, se disponivel.",
            },
        ),
    )
    @admin.display(description="Link", boolean=True)
    def link_disponivel(self, obj):
        return bool(obj.link)

    @admin.display(description="Imagem", boolean=True)
    def imagem_disponivel(self, obj):
        return bool(obj.imagem)

    @admin.display(description="Preview")
    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" alt="Preview de {}" style="max-height: 140px; border-radius: 12px;" />',
                obj.imagem.url,
                obj.nome,
            )
        return "Nenhuma imagem enviada."


class ImagemPublicacaoEstudoInline(TabularInline):
    model = ImagemPublicacaoEstudo
    extra = 1
    fields = ("imagem", "legenda", "ordem", "preview_imagem")
    readonly_fields = ("preview_imagem",)

    @admin.display(description="Preview")
    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" alt="{}" style="max-height: 90px; border-radius: 10px;" />',
                obj.imagem.url,
                obj.legenda or obj.publicacao.titulo,
            )
        return "-"


class ImagemExperienciaProfissionalInline(TabularInline):
    model = ImagemExperienciaProfissional
    extra = 1
    fields = ("imagem", "legenda", "ordem", "preview_imagem")
    readonly_fields = ("preview_imagem",)

    @admin.display(description="Preview")
    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" alt="{}" style="max-height: 90px; border-radius: 10px;" />',
                obj.imagem.url,
                obj.legenda or obj.experiencia.titulo,
            )
        return "-"


@admin.register(EmpresaProfissional)
class EmpresaProfissionalAdmin(ModelAdmin):
    list_display = ("nome", "cargo", "periodo", "ordem", "total_experiencias", "criado_em")
    list_filter = ("criado_em",)
    search_fields = ("nome", "cargo", "periodo", "descricao_curta")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("ordem", "-criado_em", "nome")
    list_per_page = 20
    readonly_fields = ("criado_em", "preview_logo")
    save_on_top = True
    fieldsets = (
        (
            "Empresa e contexto",
            {
                "fields": ("nome", "slug", "logo", "preview_logo", "cargo", "periodo"),
                "description": "Registre a empresa como parte da sua trajetoria de aprendizado profissional.",
            },
        ),
        (
            "Apresentacao publica",
            {
                "fields": ("descricao_curta", "ordem"),
                "description": "Use um texto curto focado em contexto, aprendizado e evolucao.",
            },
        ),
        (
            "Registro",
            {
                "fields": ("criado_em",),
            },
        ),
    )

    @admin.display(description="Experiencias")
    def total_experiencias(self, obj):
        return obj.experiencias.count()

    @admin.display(description="Logo")
    def preview_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" alt="{}" style="max-height: 90px; border-radius: 12px;" />',
                obj.logo.url,
                obj.nome,
            )
        return "Nenhuma logo enviada."


@admin.register(ExperienciaProfissional)
class ExperienciaProfissionalAdmin(ModelAdmin):
    list_display = (
        "titulo",
        "empresa",
        "status",
        "imagem_disponivel",
        "criado_em",
        "atualizado_em",
    )
    list_filter = ("status", "empresa", "criado_em", "atualizado_em")
    search_fields = (
        "titulo",
        "resumo",
        "atividades_realizadas",
        "aprendizados_obtidos",
        "habilidades_desenvolvidas",
        "ferramentas_competencias",
        "desafios_enfrentados",
        "resultados_alcancados",
    )
    prepopulated_fields = {"slug": ("titulo",)}
    autocomplete_fields = ("empresa",)
    ordering = ("-criado_em", "titulo")
    date_hierarchy = "criado_em"
    list_per_page = 12
    readonly_fields = ("criado_em", "atualizado_em", "preview_imagem")
    save_on_top = True
    inlines = (ImagemExperienciaProfissionalInline,)
    fieldsets = (
        (
            "Identificacao",
            {
                "fields": ("empresa", "titulo", "slug", "resumo", "status"),
            },
        ),
        (
            "Historia da experiencia",
            {
                "fields": (
                    "atividades_realizadas",
                    "aprendizados_obtidos",
                    "habilidades_desenvolvidas",
                ),
                "description": "Priorize aprendizados, evolucao e competencias desenvolvidas, nao uma lista fria de curriculo.",
            },
        ),
        (
            "Ferramentas, desafios e resultados",
            {
                "fields": (
                    "ferramentas_competencias",
                    "desafios_enfrentados",
                    "resultados_alcancados",
                ),
            },
        ),
        (
            "Midia",
            {
                "fields": ("imagem_principal", "preview_imagem"),
            },
        ),
        (
            "Registro",
            {
                "fields": ("criado_em", "atualizado_em"),
            },
        ),
    )

    @admin.display(description="Imagem", boolean=True)
    def imagem_disponivel(self, obj):
        return bool(obj.imagem_principal)

    @admin.display(description="Preview")
    def preview_imagem(self, obj):
        if obj.imagem_principal:
            return format_html(
                '<img src="{}" alt="{}" style="max-height: 140px; border-radius: 12px;" />',
                obj.imagem_principal.url,
                obj.titulo,
            )
        return "Nenhuma imagem enviada."


@admin.register(TemaEstudo)
class TemaEstudoAdmin(ModelAdmin):
    list_display = ("titulo", "ativo", "ordem", "total_publicacoes", "criado_em")
    list_filter = ("ativo", "criado_em")
    search_fields = ("titulo", "descricao_curta")
    prepopulated_fields = {"slug": ("titulo",)}
    ordering = ("ordem", "titulo")
    list_per_page = 20
    readonly_fields = ("criado_em", "preview_imagem")
    save_on_top = True
    fieldsets = (
        (
            "Tema",
            {
                "fields": ("titulo", "slug", "descricao_curta"),
                "description": "Cadastre areas de estudo como Excel, SQL, Power BI, Suporte TI ou Django.",
            },
        ),
        (
            "Exibicao",
            {
                "fields": ("imagem_capa", "preview_imagem", "ativo", "ordem"),
            },
        ),
        (
            "Registro",
            {
                "fields": ("criado_em",),
            },
        ),
    )

    @admin.display(description="Publicacoes")
    def total_publicacoes(self, obj):
        return obj.publicacoes.count()

    @admin.display(description="Preview")
    def preview_imagem(self, obj):
        if obj.imagem_capa:
            return format_html(
                '<img src="{}" alt="{}" style="max-height: 120px; border-radius: 12px;" />',
                obj.imagem_capa.url,
                obj.titulo,
            )
        return "Nenhuma imagem enviada."


@admin.register(PublicacaoEstudo)
class PublicacaoEstudoAdmin(ModelAdmin):
    list_display = (
        "titulo",
        "tema",
        "status",
        "video_disponivel",
        "imagem_disponivel",
        "criado_em",
        "atualizado_em",
    )
    list_filter = ("status", "tema", "criado_em", "atualizado_em")
    search_fields = (
        "titulo",
        "resumo",
        "conteudo",
        "tecnologias_utilizadas",
        "aprendizados_principais",
    )
    prepopulated_fields = {"slug": ("titulo",)}
    autocomplete_fields = ("tema",)
    ordering = ("-criado_em", "titulo")
    date_hierarchy = "criado_em"
    list_per_page = 12
    readonly_fields = ("criado_em", "atualizado_em", "preview_imagem")
    save_on_top = True
    inlines = (ImagemPublicacaoEstudoInline,)
    fieldsets = (
        (
            "Identificacao",
            {
                "fields": ("tema", "titulo", "slug", "resumo", "status"),
            },
        ),
        (
            "Conteudo",
            {
                "fields": ("conteudo",),
                "description": "Use este campo para registrar o que voce estudou, praticou e aprendeu.",
            },
        ),
        (
            "Midia",
            {
                "fields": ("imagem_principal", "preview_imagem", "video_url", "video_arquivo"),
                "description": "Use link externo para YouTube ou envie um arquivo de video quando fizer sentido.",
            },
        ),
        (
            "Reflexao do estudo",
            {
                "fields": (
                    "tecnologias_utilizadas",
                    "aprendizados_principais",
                    "dificuldades_encontradas",
                    "solucao_aplicada",
                ),
            },
        ),
        (
            "Registro",
            {
                "fields": ("criado_em", "atualizado_em"),
            },
        ),
    )

    @admin.display(description="Video", boolean=True)
    def video_disponivel(self, obj):
        return bool(obj.video_url or obj.video_arquivo)

    @admin.display(description="Imagem", boolean=True)
    def imagem_disponivel(self, obj):
        return bool(obj.imagem_principal)

    @admin.display(description="Preview")
    def preview_imagem(self, obj):
        if obj.imagem_principal:
            return format_html(
                '<img src="{}" alt="{}" style="max-height: 140px; border-radius: 12px;" />',
                obj.imagem_principal.url,
                obj.titulo,
            )
        return "Nenhuma imagem enviada."
