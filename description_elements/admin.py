from django.contrib import admin
from .models import Author, Translator, Location, EncompassingBibliographicUnit, Periodical


class EncompassingBibliographicUnitAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']


class PeriodicalAdmin(admin.ModelAdmin):
    exclude = ['sorting_name']


admin.site.register(Author)
admin.site.register(Translator)
admin.site.register(Location)
admin.site.register(EncompassingBibliographicUnit, EncompassingBibliographicUnitAdmin)
admin.site.register(Periodical, PeriodicalAdmin)
