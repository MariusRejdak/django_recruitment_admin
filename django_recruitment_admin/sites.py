from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.urls import include, re_path
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string
from django_recruitment_admin.models import ModelAdmin
from django_recruitment_admin.serializers import get_serializer
from rest_framework import routers


class AlreadyRegistered(Exception):
    pass


class AdminSite:
    """Django DRF Admin Panel site"""

    def __init__(self, name="admin"):
        self.name = name
        self._registry = {}

    def register(self, model_or_iterable, admin_class=None):
        """Register model for given Admin Panel site"""
        admin_class = admin_class or ModelAdmin
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    f"The model {model.__name__} is abstract, so it cannot be registered with admin."
                )

            if model in self._registry:
                raise AlreadyRegistered(
                    f"The model {model.__name__} is already registered"
                )
            self._registry[model] = admin_class(model)

    def get_urls(self):
        """Generate routes for django urlpatterns"""
        router = routers.DefaultRouter()
        for model, admin_obj in self._registry.items():
            name = admin_obj.name or str(model._meta.verbose_name_plural)
            router.register(name, get_serializer(admin_obj), base_name=model.__name__)
        return [re_path(r"^", include(router.urls))]

    @property
    def urls(self):
        return self.get_urls(), "admin", self.name


class DefaultAdminSite(LazyObject):

    def _setup(self):
        AdminSiteClass = import_string(
            apps.get_app_config("django_recruitment_admin").default_site
        )
        self._wrapped = AdminSiteClass()


default_site = DefaultAdminSite()
