# Django REST Admin Panel
Recruitment task

## Running example
```
docker-compose build
docker-compose run example migrate
docker-compose run example createsuperuser --email admin@example.com --username admin
docker-compose up
```

## Running tests
```
docker-compose build
docker-compose run example test
```

## Using library
### Instalation
* `pip install git+https://github.com/mariusrejdak/django_recruitment_admin#egg=django_recruitment_admin`
* Add `rest_framework` and `django_recruitment_admin` to `INSTALLED_APPS` in `settings.py`

### Register models in `admin.py`
```python
import django_recruitment_admin as admin
from myapp.models import Model

# Simple register
admin.site.register(Model)

# Decorate with customisation
@admin.register(Model, site=admin.site)
class ModelAdmin(admin.ModelAdmin):
    read_only_fields = ("slug",)
```

### Posible params for `admin.ModelAdmin`
* `name`    Override url endpoint and resource name, default is model name.
* `fields`  Included fields, all by default.
* `exclude` Excluded fields, none by default.
* `read_only_fields`    Fields marked as read-only.
* `permission_classes`  List of rest_framework.permissions classes.
* `readonly`    Disables creating, editing and deliting objects.

### Check example folder for more
[example](https://github.com/MariusRejdak/django_recruitment_admin/tree/master/example)
