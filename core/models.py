from django.db import models

class Projeto(models.Model):
    TIPO_CHOICES = [
        ('real', 'Projeto Real'),
        ('futuro', 'Projeto Futuro'),
    ]
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    link = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='real')

    def __str__(self):
        return self.nome
    

class Tag(models.Model):
    nome = models.CharField(max_length=50)

class Certificado(models.Model):
    nome = models.CharField(max_length=150)
    instituicao = models.CharField(max_length=100)
    data = models.DateField()
    link = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='certificados/', blank=True, null=True)



    def __str__(self):
        return self.nome   