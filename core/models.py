from urllib.parse import parse_qs, urlparse

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Projeto(models.Model):
    TIPO_CHOICES = [
        ('real', 'Projeto Real'),
        ('futuro', 'Projeto Futuro'),
    ]
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    problema_resolvido = models.TextField(blank=True)
    aprendizado_obtido = models.TextField(blank=True)
    proximos_passos = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='real')

    def __str__(self):
        return self.nome


class Tag(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.nome


class Certificado(models.Model):
    nome = models.CharField(max_length=150)
    instituicao = models.CharField(max_length=100)
    data = models.DateField()
    link = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='certificados/', blank=True, null=True)
    def __str__(self):
        return self.nome


class TemaEstudo(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    descricao_curta = models.TextField(max_length=300)
    imagem_capa = models.ImageField(upload_to='lab/temas/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('ordem', 'titulo')
        verbose_name = 'Tema de estudo'
        verbose_name_plural = 'Temas de estudo'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tema_estudo_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.titulo


class PublicacaoEstudo(models.Model):
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    ]

    tema = models.ForeignKey(
        TemaEstudo,
        on_delete=models.CASCADE,
        related_name='publicacoes',
    )
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, blank=True)
    resumo = models.TextField(max_length=400)
    conteudo = models.TextField()
    imagem_principal = models.ImageField(upload_to='lab/publicacoes/', blank=True, null=True)
    video_url = models.URLField('Link externo do video', blank=True, null=True)
    video_arquivo = models.FileField(upload_to='lab/videos/', blank=True, null=True)
    tecnologias_utilizadas = models.TextField(blank=True)
    aprendizados_principais = models.TextField(blank=True)
    dificuldades_encontradas = models.TextField(blank=True)
    solucao_aplicada = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rascunho')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-criado_em', 'titulo')
        unique_together = ('tema', 'slug')
        verbose_name = 'Publicacao de estudo'
        verbose_name_plural = 'Publicacoes de estudo'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'publicacao_estudo_detail',
            kwargs={'tema_slug': self.tema.slug, 'slug': self.slug},
        )

    @property
    def tecnologias_lista(self):
        return [item.strip() for item in self.tecnologias_utilizadas.split(',') if item.strip()]

    @property
    def video_embed_url(self):
        if not self.video_url:
            return ''

        parsed = urlparse(self.video_url)
        host = parsed.netloc.lower()

        if 'youtube.com' in host:
            video_id = parse_qs(parsed.query).get('v', [''])[0]
            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'

        if 'youtu.be' in host:
            video_id = parsed.path.strip('/')
            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'

        return ''

    def __str__(self):
        return self.titulo


class ImagemPublicacaoEstudo(models.Model):
    publicacao = models.ForeignKey(
        PublicacaoEstudo,
        on_delete=models.CASCADE,
        related_name='imagens_extras',
    )
    imagem = models.ImageField(upload_to='lab/galeria/')
    legenda = models.CharField(max_length=150, blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('ordem', 'id')
        verbose_name = 'Imagem extra da publicacao'
        verbose_name_plural = 'Imagens extras da publicacao'

    def __str__(self):
        return self.legenda or f'Imagem de {self.publicacao}'


class EmpresaProfissional(models.Model):
    nome = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    logo = models.ImageField(upload_to='profissional/empresas/', blank=True, null=True)
    cargo = models.CharField(max_length=120)
    periodo = models.CharField('periodo', max_length=80)
    descricao_curta = models.TextField(max_length=350)
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('ordem', '-criado_em', 'nome')
        verbose_name = 'Empresa profissional'
        verbose_name_plural = 'Empresas profissionais'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('empresa_profissional_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.nome


class ExperienciaProfissional(models.Model):
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    ]

    empresa = models.ForeignKey(
        EmpresaProfissional,
        on_delete=models.CASCADE,
        related_name='experiencias',
    )
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, blank=True)
    resumo = models.TextField(max_length=450)
    atividades_realizadas = models.TextField()
    aprendizados_obtidos = models.TextField()
    habilidades_desenvolvidas = models.TextField(blank=True)
    ferramentas_competencias = models.TextField(
        'tecnologias, ferramentas e competencias utilizadas',
        blank=True,
    )
    desafios_enfrentados = models.TextField(blank=True)
    resultados_alcancados = models.TextField(blank=True)
    imagem_principal = models.ImageField(upload_to='profissional/experiencias/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rascunho')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-criado_em', 'titulo')
        unique_together = ('empresa', 'slug')
        verbose_name = 'Experiencia profissional'
        verbose_name_plural = 'Experiencias profissionais'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    @property
    def ferramentas_lista(self):
        return [item.strip() for item in self.ferramentas_competencias.split(',') if item.strip()]

    def __str__(self):
        return self.titulo


class ImagemExperienciaProfissional(models.Model):
    experiencia = models.ForeignKey(
        ExperienciaProfissional,
        on_delete=models.CASCADE,
        related_name='imagens',
    )
    imagem = models.ImageField(upload_to='profissional/galeria/')
    legenda = models.CharField(max_length=150, blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('ordem', 'id')
        verbose_name = 'Imagem da experiencia profissional'
        verbose_name_plural = 'Imagens da experiencia profissional'

    def __str__(self):
        return self.legenda or f'Imagem de {self.experiencia}'
