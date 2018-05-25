from django.utils.module_loading import autodiscover_modules
from django_recruitment_admin.decorators import register
from django_recruitment_admin.models import ModelAdmin
from django_recruitment_admin.sites import AdminSite, default_site as site


def autodiscover():
    """Finds and imports all admin modules in apps"""
    autodiscover_modules("admin", register_to=site)


default_app_config = "django_recruitment_admin.apps.AdminConfig"
