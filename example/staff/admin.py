import django_recruitment_admin as admin
from staff.models import Department, Employee, Project
from rest_framework.permissions import AllowAny, IsAuthenticated


# Admin panel for HR
# Default admin panel

admin.site.register(Department)
admin.site.register(Employee)


@admin.register(Project, site=admin.site)
class ProjectAdmin(admin.ModelAdmin):
    read_only_fields = ("start_date",)


# Availible for everyone
# Custom admin panel

public_site = admin.AdminSite("public-portal")


@admin.register(Department, site=public_site)
class DepartmentPublic(admin.ModelAdmin):
    readonly = True
    permission_classes = (AllowAny,)


@admin.register(Employee, site=public_site)
class EmployeePublic(admin.ModelAdmin):
    fields = ("first_name", "last_name")
    readonly = True
    permission_classes = (IsAuthenticated,)


@admin.register(Project, site=public_site)
class ProjectPublic(admin.ModelAdmin):
    exclude = ("description", "hidden")
    readonly = True
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Filter confidential data"""
        return self.model.objects.filter(hidden=False)
