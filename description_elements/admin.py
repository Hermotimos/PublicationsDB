from django.contrib import admin
from .models import Author, Translator, Location, Keyword, EncompassingBibliographicUnit, Periodical


class AuthorAdmin(admin.ModelAdmin):
    exclude = []
    search_fields = ['first_names', 'last_name']


class TranslatorAdmin(admin.ModelAdmin):
    exclude = []
    search_fields = ['first_names', 'last_name']


class KeywordAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['id', 'name']
    list_display_links = ['id']
    list_editable = ['name']
    search_fields = ['name']


class LocationAdmin(admin.ModelAdmin):
    exclude = []
    search_fields = ['name']


class EncompassingBibliographicUnitAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']


class PeriodicalAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(EncompassingBibliographicUnit, EncompassingBibliographicUnitAdmin)
admin.site.register(Periodical, PeriodicalAdmin)
