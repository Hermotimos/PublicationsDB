from django.contrib import admin
from .models import CategoryLevelOne, CategoryLevelTwo, CategoryLevelThree


class CategoryLevelTwoInline(admin.TabularInline):
    model = CategoryLevelTwo
    extra = 5
    verbose_name = 'Kategorie poz. 2 w ramach wybranej Kategorii poz. 1'
    verbose_name_plural = 'Kategorie poz. 2 w ramach wybranej Kategorii poz. 1 (istniejące + puste pola do wprowadzenia nowych)'


class CategoryLevelThreeInline(admin.TabularInline):
    model = CategoryLevelThree
    extra = 5
    verbose_name = 'Kategorie poz. 3 w ramach wybranej Kategorii poz. 2'
    verbose_name_plural = 'Kategorie poz. 3 w ramach wybranej Kategorii poz. 2 (istniejące + puste pola do wprowadzenia nowych)'


class CategoryLevelOneAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [CategoryLevelTwoInline, ]


class CategoryLevelTwoAdmin(admin.ModelAdmin):
    list_display = ['get_cat_lvl_2_str', 'get_cat_lvl_1_name', 'get_cat_lvl_2_name']
    inlines = [CategoryLevelThreeInline, ]

    def get_cat_lvl_2_str(self, obj):
        return obj

    def get_cat_lvl_1_name(self, obj):
        return str(obj.cat_lvl_1)

    def get_cat_lvl_2_name(self, obj):
        return str(obj.name)

    get_cat_lvl_1_name.short_description = 'Kategoria poz. 1'
    get_cat_lvl_2_name.short_description = 'Kategoria poz. 2'
    get_cat_lvl_2_str.short_description = 'Pełna ścieżka kategorii poz. 2'


class CategoryLevelThreeAdmin(admin.ModelAdmin):
    list_display = ['get_cat_lvl_3_str', 'get_cat_lvl_1_name', 'get_cat_lvl_2_name', 'get_cat_lvl_3_name']

    def get_cat_lvl_3_str(self, obj):
        return obj

    def get_cat_lvl_1_name(self, obj):
        return str(obj.cat_lvl_2.cat_lvl_1)

    def get_cat_lvl_2_name(self, obj):
        return str(obj.cat_lvl_2.name)

    def get_cat_lvl_3_name(self, obj):
        return str(obj.name)

    get_cat_lvl_1_name.short_description = 'Kategoria poz. 1'
    get_cat_lvl_2_name.short_description = 'Kategoria poz. 2'
    get_cat_lvl_3_name.short_description = 'Kategoria poz. 3'
    get_cat_lvl_3_str.short_description = 'Pełna ścieżka kategorii poz. 3'


admin.site.register(CategoryLevelOne, CategoryLevelOneAdmin)
admin.site.register(CategoryLevelTwo, CategoryLevelTwoAdmin)
admin.site.register(CategoryLevelThree, CategoryLevelThreeAdmin)
