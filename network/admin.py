from django.contrib import admin

from network.models import Company, Product


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier', 'country', 'city')
    list_display_links = ('supplier',)
    list_filter = ('name', 'city')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'release_date')
    list_filter = ('name',)
