from django.utils import timezone
from .models import SiteSettings, Service

def site_settings(request):
    settings = SiteSettings.objects.first()
    # Process copyright text to replace {year} with current year
    copyright_text = settings.copyright_text if settings else "© {year} Villa Grande Lodge. All rights reserved."
    current_year = timezone.now().year
    copyright_processed = copyright_text.replace("{year}", str(current_year))

    return {
        'site_settings': settings,
        'services': Service.objects.filter(is_active=True).order_by('order'),
        'copyright_text': copyright_processed,   # added processed copyright
    }