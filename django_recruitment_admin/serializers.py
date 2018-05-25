from rest_framework import serializers, viewsets


def get_serializer(admin_model):
    """Creates Serializer and ViewSet to expose the Model via DRF"""

    class ModelSerializer(serializers.ModelSerializer):

        class Meta:
            model = admin_model.model
            read_only_fields = admin_model.read_only_fields

    if admin_model.exclude:
        ModelSerializer.Meta.exclude = admin_model.exclude
    else:
        ModelSerializer.Meta.fields = admin_model.fields

    viewset_class = (
        viewsets.ReadOnlyModelViewSet if admin_model.readonly else viewsets.ModelViewSet
    )
    viewset_attr = {
        "serializer_class": ModelSerializer,
        "permission_classes": admin_model.permission_classes,
        "queryset": admin_model.model.objects.none(),  # Required for DjangoModelPermissions
        "get_queryset": admin_model.get_queryset,
    }

    # Construct ViewSet class
    return type(f"{admin_model.model.__name__}ViewSet", (viewset_class,), viewset_attr)
