"""Borrowed form django.contrib.admin"""

from django_recruitment_admin.models import ModelAdmin
from django_recruitment_admin.sites import default_site, AdminSite


def register(*models, site=None):
    """Decorator for registering models by annotating ModelAdmin classes"""

    def _model_admin_wrapper(admin_class):
        if not models:
            raise ValueError("At least one model must be passed to register.")

        admin_site = site or default_site

        if not isinstance(admin_site, AdminSite):
            raise ValueError("site must subclass AdminSite")

        if not issubclass(admin_class, ModelAdmin):
            raise ValueError("Wrapped class must subclass ModelAdmin.")

        admin_site.register(models, admin_class=admin_class)

        return admin_class

    return _model_admin_wrapper
