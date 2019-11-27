from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

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
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(),
                                             widget=FilteredSelectMultiple('Autorzy', False),
                                             required=False,
                                             label='Autor/Autorzy')
    translators = forms.ModelMultipleChoiceField(queryset=Translator.objects.all(),
                                                 widget=FilteredSelectMultiple('Tłumacze', False),
                                                 required=False,
                                                 label='Tłumacz/Tłumacze')

    class Meta:
        model = EncompassingBibliographicUnit
        # exclude = []
        exclude = ['sorting_name', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'size': 100}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class EncompassingBibliographicUnitAdmin(admin.ModelAdmin):
    form = EncompassingBibliographicUnitAdminForm
    exclude = ['sorting_name']
    search_fields = ['title']

    def authors_(self):
        return ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''


class PeriodicalAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']
    search_fields = ['title']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(EncompassingBibliographicUnit, EncompassingBibliographicUnitAdmin)
admin.site.register(Periodical, PeriodicalAdmin)
