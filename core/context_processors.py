from django.conf import settings


def site_metadata(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL.rstrip('/'),
        'site_description': settings.SITE_DESCRIPTION,
        'site_image': f"{settings.STATIC_URL}core/img/logo.png",
    }
