from mainapp.models import SiteConfiguration


def site_settings(request):
    """настройки сайта передаем в контекст"""
    return vars(SiteConfiguration.get_solo())
