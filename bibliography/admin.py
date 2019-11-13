from django.contrib import admin
from .models import Book, Chapter, Article
from django import forms


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = []
        # exclude = ['sorting_name', 'description', ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 20}),
            'editors': forms.SelectMultiple(attrs={'size': 20}),
            'translators': forms.SelectMultiple(attrs={'size': 20}),
            'published_locations': forms.SelectMultiple(attrs={'size': 20}),
            'cat_lvl_3': forms.SelectMultiple(attrs={'size': 20}),
            'keywords': forms.SelectMultiple(attrs={'size': 20}),

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


class ChapterAdminForm(forms.ModelForm):
    class Meta:
        model = Chapter
        exclude = []
        # exclude = ['sorting_name', 'description', 'published_year', ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 20}),
            'editors': forms.SelectMultiple(attrs={'size': 20}),
            'translators': forms.SelectMultiple(attrs={'size': 20}),
            'cat_lvl_3': forms.SelectMultiple(attrs={'size': 20}),
            'keywords': forms.SelectMultiple(attrs={'size': 20}),

            'title': forms.TextInput(attrs={'size': 80}),
            'annotation': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'sorting_name': forms.TextInput(attrs={'size': 80}),
            'description': forms.TextInput(attrs={'size': 80}),

            'editors_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'in_volume': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = []
        # exclude = ['sorting_name', 'description', 'published_year', ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'size': 20}),
            'editors': forms.SelectMultiple(attrs={'size': 20}),
            'translators': forms.SelectMultiple(attrs={'size': 20}),
            'cat_lvl_3': forms.SelectMultiple(attrs={'size': 20}),
            'keywords': forms.SelectMultiple(attrs={'size': 20}),

            'title': forms.TextInput(attrs={'size': 80}),
            'annotation': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'sorting_name': forms.TextInput(attrs={'size': 80}),
            'description': forms.TextInput(attrs={'size': 80}),

            'editors_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
            'translators_abbrev': forms.TextInput(attrs={'rows': 1, 'cols': 5}),
        }


class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    search_fields = ['description']


class ChapterAdmin(admin.ModelAdmin):
    form = ChapterAdminForm
    search_fields = ['description']


class ArticlelAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    search_fields = ['description']


admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Article, ArticlelAdmin)
