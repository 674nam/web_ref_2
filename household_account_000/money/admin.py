# django-import-export 使用バージョン
# 管理サイトからデータのインポート、エクスポートを可能にする
# settings.pyのINSTALLED_APPSに'import-export'を追加
from django.contrib import admin
from .models import Payment, Income, PaymentCategory, IncomeCategory,\
                    PaymentItem, IncomeItem, PaymentOrigItem, IncomeOrigItem, Budget
from import_export import resources  # django-import-export のインストールが必要
from import_export.admin import ImportExportModelAdmin

# Paymentモデルへの統合
class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment

# 管理者画面：摘要の検索、カテゴリ絞り込み
class PaymentAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ['date', 'price', 'description']
    # list_display = ['date', 'category', 'price', 'description']
    # list_filter = ('category',)
    ordering = ('-date',)

    resource_class = PaymentResource

# PaymentCategoryモデルへの統合
class PaymentCategoryResource(resources.ModelResource):
    class Meta:
        model = PaymentCategory

# 管理者画面
class PaymentCategoryAdmin(ImportExportModelAdmin):
    resource_class = PaymentCategoryResource

# PaymentItemモデルへの統合
class PaymentItemResource(resources.ModelResource):
    class Meta:
        model = PaymentItem

# 管理者画面
class PaymentItemAdmin(ImportExportModelAdmin):
    resource_class = PaymentItemResource

# PaymentOrigItemモデルへの統合
class PaymentOrigItemResource(resources.ModelResource):
    class Meta:
        model = PaymentOrigItem

# 管理者画面
class PaymentOrigItemAdmin(ImportExportModelAdmin):
    resource_class = PaymentOrigItemResource

# Incomeモデルへの統合
class IncomeResource(resources.ModelResource):
    class Meta:
        model = Income

# 管理者画面：摘要の検索、カテゴリ絞り込み
class IncomeAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ['date', 'price', 'description']
    # list_display = ['date', 'category', 'price', 'description']
    # list_filter = ('category',)
    ordering = ('-date',)

    resource_class = IncomeResource

# IncomeCategoryモデルへの統合
class IncomeCategoryResource(resources.ModelResource):
    class Meta:
        model = IncomeCategory

# 管理者画面
class IncomeCategoryAdmin(ImportExportModelAdmin):
    resource_class = IncomeCategoryResource

# IncomeItemモデルへの統合
class IncomeItemResource(resources.ModelResource):
    class Meta:
        model = IncomeItem

# 管理者画面
class IncomeItemAdmin(ImportExportModelAdmin):
    resource_class = IncomeItemResource

# IncomeOrigItemモデルへの統合
class IncomeOrigItemResource(resources.ModelResource):
    class Meta:
        model = IncomeOrigItem

# 管理者画面
class IncomeOrigItemAdmin(ImportExportModelAdmin):
    resource_class = IncomeOrigItemResource

# Budgetモデルへの統合
class BudgetResource(resources.ModelResource):
    class Meta:
        model = Budget

# 管理者画面
class BudgetAdmin(ImportExportModelAdmin):
    resource_class = BudgetResource


admin.site.register(PaymentCategory, PaymentCategoryAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Income, IncomeAdmin)

admin.site.register(PaymentItem,PaymentItemAdmin)
admin.site.register(IncomeItem,IncomeItemAdmin)
admin.site.register(PaymentOrigItem,PaymentOrigItemAdmin)
admin.site.register(IncomeOrigItem,IncomeOrigItemAdmin)
admin.site.register(Budget,BudgetAdmin)
