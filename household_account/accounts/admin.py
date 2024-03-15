from django.contrib import admin
from django.contrib.auth.models import Group
from import_export import resources  # django-import-export のインストールが必要
from import_export.admin import ImportExportModelAdmin

from .models import User, Family

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UserAdmin(ImportExportModelAdmin):
    list_display = ("account_id", "email", "is_superuser")
    readonly_fields = ('created_at', 'updated_at')
    ordering = ("-updated_at",)
    exclude = ("username", )

    fieldsets = (
        (None, {"fields": ("account_id", "email", "first_name", "family_name",
                            "is_active", "created_at", "updated_at")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "user_permissions")}),
    )

class FamilyResource(resources.ModelResource):
    class Meta:
        model = Family

class FamilyAdmin(ImportExportModelAdmin):
    resource_class = FamilyResource

admin.site.register(User, UserAdmin)  # Userモデルを登録
admin.site.register(Family,FamilyAdmin)  # Familyモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示