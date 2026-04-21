from django.contrib import admin
from django.utils.html import format_html

from .models import Certificado, Projeto, Tag


admin.site.site_header = "Lucas Admin"
admin.site.site_title = "Painel Administrativo"
admin.site.index_title = "Gestão do Portfólio"


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "tipo",
        "tags_resumo",
        "link_disponivel",
        "imagem_disponivel",
        "criado_em",
    )
    list_filter = ("tipo", "tags", "criado_em")
    search_fields = ("nome", "descricao", "tags__nome")
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
                "fields": ("nome", "descricao"),
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
    jazzmin_section_order = (
        "Informacoes principais",
        "Classificacao e organizacao",
        "Midia e publicacao",
        "Registro",
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
class TagAdmin(admin.ModelAdmin):
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
    jazzmin_section_order = ("Identificacao da tag",)

    @admin.display(description="Projetos vinculados")
    def total_projetos(self, obj):
        return obj.projeto_set.count()


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
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
    jazzmin_section_order = ("Dados do certificado", "Comprovacao e midia")

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
