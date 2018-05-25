from rest_framework import viewsets
from rest_framework.settings import api_settings


class ModelAdmin:
    """Model configuration for admin panel endpoints

    Attributes:
        name    Override url endpoint and resource name, default is model name.
        fields  Included fields, all by default.
        exclude Excluded fields, none by default.
        read_only_fields    Fields marked as read-only.
        permission_classes  List of rest_framework.permissions classes.
        readonly    Disables creating, editing and deliting objects.
    """
    name = None
    fields = "__all__"
    exclude = tuple()
    read_only_fields = tuple()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    readonly = False

    def __init__(self, model):
        self.model = model

    def get_queryset(self):
        """Create queryset to model objects, can be used for filtering."""
        return self.model.objects.all()
