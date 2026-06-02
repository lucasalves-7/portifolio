# Lucas Alves Tech

Portfolio em Django para apresentar projetos, estudos, aprendizados profissionais e evolucao na area de TI.

## Principais recursos

- Home com posicionamento profissional, destaques, projetos, certificados e contato.
- Lab de Estudos gerenciado pelo Django Admin.
- Aprendizados Profissionais com empresas, experiencias e timeline.
- Admin com Django Unfold, filtros, buscas, previews e inlines de imagens.
- Uploads por `MEDIA_URL` e arquivos estaticos prontos para WhiteNoise.
- SEO basico com title, description, canonical, Open Graph e imagem social.

## Como rodar localmente

```bash
python -m venv env
env\Scripts\pip.exe install -r requirements.txt
env\Scripts\python.exe manage.py migrate
env\Scripts\python.exe manage.py createsuperuser
env\Scripts\python.exe manage.py runserver
```

Depois acesse:

- Site: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Dados iniciais

Para criar exemplos de projeto, tema de estudo, publicacao e experiencia profissional:

```bash
env\Scripts\python.exe manage.py seed_portfolio
```

O comando e idempotente: pode ser executado novamente sem duplicar os registros principais.

## Variaveis de ambiente

Use `.env.example` como referencia para configurar:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `SITE_NAME`
- `SITE_URL`
- `SITE_DESCRIPTION`
- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_SESSION_COOKIE_SECURE`
- `DJANGO_CSRF_COOKIE_SECURE`
- `DJANGO_SECURE_HSTS_SECONDS`

## Deploy

Checklist recomendado antes de publicar:

```bash
env\Scripts\python.exe manage.py check --deploy
env\Scripts\python.exe manage.py collectstatic
env\Scripts\python.exe manage.py test
```

Em producao, defina `DJANGO_DEBUG=False`, configure `DJANGO_ALLOWED_HOSTS`, use uma `DJANGO_SECRET_KEY` segura e sirva os uploads da pasta `media/` conforme a plataforma escolhida. As flags de HTTPS e cookies seguros ficam ativas por padrao quando `DJANGO_DEBUG=False`, mas tambem podem ser controladas por variaveis de ambiente.
