from django.contrib import admin

from .models import Category, Product, SubCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'image')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'subcategory', 'price')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('subcategory',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
