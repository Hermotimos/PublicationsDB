from django.contrib import admin
from django import forms

from .models import Author, Translator, Location, Keyword, EncompassingBibliographicUnit, Periodical


class AuthorAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']
    search_fields = ['first_names', 'last_name']


class TranslatorAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']
    search_fields = ['first_names', 'last_name']


class KeywordAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']
    list_display = ['id', 'name']
    list_display_links = ['id']
    list_editable = ['name']
    search_fields = ['name']


class LocationAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']
    search_fields = ['name']


class EncompassingBibliographicUnitAdminForm(forms.ModelForm):
    class Meta:
        model = EncompassingBibliographicUnit
        # exclude = []
        exclude = ['sorting_name', 'description']
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 20}),

            'translators': forms.SelectMultiple(attrs={'size': 20}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class EncompassingBibliographicUnitAdmin(admin.ModelAdmin):
    form = EncompassingBibliographicUnitAdminForm
    exclude = ['sorting_name']


class PeriodicalAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(EncompassingBibliographicUnit, EncompassingBibliographicUnitAdmin)
admin.site.register(Periodical, PeriodicalAdmin)
