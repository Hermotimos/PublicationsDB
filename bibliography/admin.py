from django.contrib import admin
from .models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical
from django import forms


class BibliographicUnitBookAdminForm(forms.ModelForm):
    class Meta:
        model = BibliographicUnitBook
        exclude = ['sorting_name', 'description', ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 20}),
            'editors': forms.SelectMultiple(attrs={'size': 20}),
            'translators': forms.SelectMultiple(attrs={'size': 20}),
            'published_locations': forms.SelectMultiple(attrs={'size': 20}),
            'cat_lvl_3': forms.SelectMultiple(attrs={'size': 20}),

            'title': forms.TextInput(attrs={'size': 80}),
            'annotation': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'sorting_name': forms.TextInput(attrs={'size': 80}),
            'description': forms.TextInput(attrs={'size': 80}),

            'editors_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'published_year': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'volumes': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'edition': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class BibliographicUnitPartOfBookAdminForm(forms.ModelForm):
    class Meta:
        model = BibliographicUnitBook
        exclude = ['sorting_name', 'description', 'published_year', ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 20}),
            'editors': forms.SelectMultiple(attrs={'size': 20}),
            'translators': forms.SelectMultiple(attrs={'size': 20}),
            'cat_lvl_3': forms.SelectMultiple(attrs={'size': 20}),

            'title': forms.TextInput(attrs={'size': 80}),
            'annotation': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'sorting_name': forms.TextInput(attrs={'size': 80}),
            'description': forms.TextInput(attrs={'size': 80}),

            'editors_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'in_volume': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class BibliographicUnitPartOfPeriodicalAdminForm(forms.ModelForm):
    class Meta:
        model = BibliographicUnitBook
        exclude = ['sorting_name', 'description', 'published_year', ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 20}),
            'editors': forms.SelectMultiple(attrs={'size': 20}),
            'translators': forms.SelectMultiple(attrs={'size': 20}),
            'cat_lvl_3': forms.SelectMultiple(attrs={'size': 20}),

            'title': forms.TextInput(attrs={'size': 80}),
            'annotation': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'sorting_name': forms.TextInput(attrs={'size': 80}),
            'description': forms.TextInput(attrs={'size': 80}),

            'editors_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class BibliographicUnitBookAdmin(admin.ModelAdmin):
    form = BibliographicUnitBookAdminForm


class BibliographicUnitPartOfBookAdmin(admin.ModelAdmin):
    form = BibliographicUnitPartOfBookAdminForm


class BibliographicUnitPartOfPeriodicalAdmin(admin.ModelAdmin):
    form = BibliographicUnitPartOfPeriodicalAdminForm


admin.site.register(BibliographicUnitBook, BibliographicUnitBookAdmin)
admin.site.register(BibliographicUnitPartOfBook, BibliographicUnitPartOfBookAdmin)
admin.site.register(BibliographicUnitPartOfPeriodical, BibliographicUnitPartOfPeriodicalAdmin)
