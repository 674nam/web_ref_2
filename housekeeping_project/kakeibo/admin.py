# # django-import-export 不使用バージョン
# # settings.pyのINSTALLED_APPSから'import-export'を削除orコメントアウト
# from django.contrib import admin
# from .models import Payment, Income, PaymentCategory, IncomeCategory

# class PaymentAdmin(admin.ModelAdmin): # 管理者画面：摘要の検索、カテゴリ絞り込み
#     search_fields = ('description',)
#     list_display = ['date', 'category', 'price', 'description']
#     list_filter = ('category',)
#     ordering = ('-date',)

# class IncomeAdmin(admin.ModelAdmin): # 管理者画面：摘要の検索、カテゴリ絞り込み
#     search_fields = ('description',)
#     list_display = ['date', 'category', 'price', 'description']
#     list_filter = ('category',)
#     ordering = ('-date',)

# admin.site.register(Payment, PaymentAdmin)
# admin.site.register(Income, IncomeAdmin)
# admin.site.register(PaymentCategory)
# admin.site.register(IncomeCategory)

# django-import-export 使用バージョン
# 管理サイトからデータのインポート、エクスポートを可能にする
# settings.pyのINSTALLED_APPSに'import-export'を追加
from django.contrib import admin
from .models import Payment, Income, PaymentCategory, IncomeCategory
from import_export import resources  # django-import-export のインストールが必要
from import_export.admin import ImportExportModelAdmin

class PaymentResource(resources.ModelResource):  # Paymentモデルへの統合
    class Meta:
        model = Payment


class PaymentAdmin(ImportExportModelAdmin): # 管理者画面：摘要の検索、カテゴリ絞り込み
    search_fields = ('description',)
    list_display = ['date', 'category', 'price', 'description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = PaymentResource


class PaymentCategoryResource(resources.ModelResource): # PaymentCategoryモデルへの統合
    class Meta:
        model = PaymentCategory


class PaymentCategoryAdmin(ImportExportModelAdmin): # 管理者画面

    resource_class = PaymentCategoryResource


class IncomeResource(resources.ModelResource): # Incomeモデルへの統合
    class Meta:
        model = Income


class IncomeAdmin(ImportExportModelAdmin): # 管理者画面：摘要の検索、カテゴリ絞り込み
    search_fields = ('description',)
    list_display = ['date', 'category', 'price', 'description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = IncomeResource


class IncomeCategoryResource(resources.ModelResource): # IncomeCategoryモデルへの統合
    class Meta:
        model = IncomeCategory


class IncomeCategoryAdmin(ImportExportModelAdmin): # 管理者画面
    resource_class = IncomeCategoryResource


admin.site.register(PaymentCategory, PaymentCategoryAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Income, IncomeAdmin)