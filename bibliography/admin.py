from django.contrib import admin
from .models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical

admin.site.register(BibliographicUnitBook)
admin.site.register(BibliographicUnitPartOfBook)
admin.site.register(BibliographicUnitPartOfPeriodical)
