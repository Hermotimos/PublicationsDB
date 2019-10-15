from django.contrib import admin
from .models import Author, Location, BibliographicUnit

admin.site.register(Author)
admin.site.register(Location)
admin.site.register(BibliographicUnit)
