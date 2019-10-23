from django.contrib import admin
from .models import Author, Translator, Location, EncompassingBibliographicUnit, Periodical

admin.site.register(Author)
admin.site.register(Translator)
admin.site.register(Location)
admin.site.register(EncompassingBibliographicUnit)
admin.site.register(Periodical)
