from django.contrib import admin
from .models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical, \
    EncompassingBibliographicUnit, Periodical

admin.site.register(BibliographicUnitBook)
admin.site.register(BibliographicUnitPartOfBook)
admin.site.register(BibliographicUnitPartOfPeriodical)
admin.site.register(EncompassingBibliographicUnit)
admin.site.register(Periodical)
