from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from bibliography.models import Book, Chapter, Article
from categories.models import CategoryLevelThree
from description_elements.models import Author, Translator, Location, Keyword


class BookAdminForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(),
                                             widget=FilteredSelectMultiple('Autorzy', False),
                                             required=False,
                                             label='Autor/Autorzy')
    editors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(),
                                             widget=FilteredSelectMultiple('Redaktorzy', False),
                                             required=False,
                                             label='Redaktor/Redaktorzy')
    translators = forms.ModelMultipleChoiceField(queryset=Translator.objects.all(),
                                                 widget=FilteredSelectMultiple('Tłumacze', False),
                                                 required=False,
                                                 label='Tłumacz/Tłumacze')
    published_locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(),
                                                         widget=FilteredSelectMultiple('Miejsca wydania', False),
                                                         required=False,
                                                         label='Miejsce/miejsca wydania')
    cat_lvl_3 = forms.ModelMultipleChoiceField(queryset=CategoryLevelThree.objects.all(),
                                               widget=FilteredSelectMultiple('Kategorie i podkategorie', False),
                                               required=False,
                                               label='Kategorie i podkategorie')
    keywords = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all(),
                                              widget=FilteredSelectMultiple('Wyrażenia kluczowe', False),
                                              required=False,
                                              label='Wyrażenia kluczowe')

    class Meta:
        model = Book
        # exclude = []
        exclude = ['sorting_name', 'description']
        widgets = {
            'annotation': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
            'editors_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'published_year': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'title': forms.TextInput(attrs={'size': 100}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'volumes': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class ChapterAdminForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(),
                                             widget=FilteredSelectMultiple('Autorzy', False),
                                             required=False,
                                             label='Autor/Autorzy')
    editors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(),
                                             widget=FilteredSelectMultiple('Redaktorzy', False),
                                             required=False,
                                             label='Redaktor/Redaktorzy')
    published_locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(),
                                                         widget=FilteredSelectMultiple('Miejsca wydania', False),
                                                         required=False,
                                                         label='Miejsce/miejsca wydania')
    cat_lvl_3 = forms.ModelMultipleChoiceField(queryset=CategoryLevelThree.objects.all(),
                                               widget=FilteredSelectMultiple('Kategorie i podkategorie', False),
                                               required=False,
                                               label='Kategorie i podkategorie')
    keywords = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all(),
                                              widget=FilteredSelectMultiple('Wyrażenia kluczowe', False),
                                              required=False,
                                              label='Wyrażenia kluczowe')

    class Meta:
        model = Chapter
        # exclude = []
        exclude = ['sorting_name', 'description']
        widgets = {
            'annotation': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
            'editors_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'in_volume': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'published_year': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'title': forms.TextInput(attrs={'size': 100}),
        }


class ArticleAdminForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(),
                                             widget=FilteredSelectMultiple('Autorzy', False),
                                             required=False,
                                             label='Autor/Autorzy')
    cat_lvl_3 = forms.ModelMultipleChoiceField(queryset=CategoryLevelThree.objects.all(),
                                               widget=FilteredSelectMultiple('Kategorie i podkategorie', False),
                                               required=False,
                                               label='Kategorie i podkategorie')
    keywords = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all(),
                                              widget=FilteredSelectMultiple('Wyrażenia kluczowe', False),
                                              required=False,
                                              label='Wyrażenia kluczowe')

    class Meta:
        model = Article
        # exclude = []
        exclude = ['sorting_name', 'description', 'published_year']
        widgets = {
            'annotation': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
            'authors': forms.SelectMultiple(attrs={'size': 20}),
            'cat_lvl_3': forms.SelectMultiple(attrs={'size': 20}),
            'keywords': forms.SelectMultiple(attrs={'size': 20}),
            'title': forms.TextInput(attrs={'size': 100}),
        }


class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    search_fields = ['description']


class ChapterAdmin(admin.ModelAdmin):
    form = ChapterAdminForm
    search_fields = ['description']


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    search_fields = ['description']


admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Article, ArticleAdmin)
