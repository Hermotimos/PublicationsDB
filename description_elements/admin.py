from django.contrib import admin
from .models import Author, Translator, Location, EncompassingBibliographicUnit, Periodical


class EncompassingBibliographicUnitAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']


class PeriodicalAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']


class AuthorAdmin(admin.ModelAdmin):
    exclude = []
    search_fields = ['first_names', 'last_name']


class TranslatorAdmin(admin.ModelAdmin):
    exclude = []
    search_fields = ['first_names', 'last_name']


class LocationAdmin(admin.ModelAdmin):
    exclude = []
    search_fields = ['name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(EncompassingBibliographicUnit, EncompassingBibliographicUnitAdmin)
admin.site.register(Periodical, PeriodicalAdmin)
