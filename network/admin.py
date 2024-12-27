from django.contrib import admin
from network.models import Company, Product


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier', 'country', 'city', 'company_level')
    list_display_links = ('id', 'supplier',)
    list_filter = ('city',)

    actions = ('reset_debt',)

    @admin.action(description='Очистить значение "Задолженность перед поставщиком"')
    def reset_debt(self, request, queryset):
        queryset.update(debt=0)
        self.message_user(request, 'Значение "Задолженность перед поставщиком" успешно приведено к нулю.')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'release_date')
    list_filter = ('name',)
