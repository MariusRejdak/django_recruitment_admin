from django.apps import AppConfig


class SimpleAdminConfig(AppConfig):
    """App config without module autodiscovery"""
    name = "django_recruitment_admin"
    verbose_name = "DRF Admin"
    default_site = "django_recruitment_admin.sites.AdminSite"


class AdminConfig(SimpleAdminConfig):
    """App config with module autodiscovery"""

    def ready(self):
        self.module.autodiscover()
