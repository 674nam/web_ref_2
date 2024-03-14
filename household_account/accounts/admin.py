from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Family

class UserAdmin(admin.ModelAdmin): # 管理者画面
    list_display = ("account_id", "email", "is_superuser")
    readonly_fields = ('created_at', 'updated_at')
    ordering = ("-updated_at",)
    exclude = ("username", )

    fieldsets = (
        (None, {"fields": ("account_id", "email", "first_name", "family_name",
                            "is_active", "created_at", "updated_at")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "user_permissions")}),
    )

admin.site.register(User, UserAdmin)  # Userモデルを登録
admin.site.register(Family)  # Familyモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示