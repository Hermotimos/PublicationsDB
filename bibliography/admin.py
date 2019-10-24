from django.contrib import admin
from .models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical


class BibliographicUnitBookAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        form.save_m2m()
        # for formset in formsets:
        #     self.save_formset(request, form, formset, change=change)
        super(BibliographicUnitBookAdmin, self).save_model(request, form.instance, form, change)


class BibliographicUnitPartOfBookAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        form.save_m2m()
        # for formset in formsets:
        #     self.save_formset(request, form, formset, change=change)
        super(BibliographicUnitPartOfBookAdmin, self).save_model(request, form.instance, form, change)


class BibliographicUnitPartOfPeriodicalAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        form.save_m2m()
        # for formset in formsets:
        #     self.save_formset(request, form, formset, change=change)
        super(BibliographicUnitPartOfPeriodicalAdmin, self).save_model(request, form.instance, form, change)


admin.site.register(BibliographicUnitBook, BibliographicUnitBookAdmin)
admin.site.register(BibliographicUnitPartOfBook, BibliographicUnitPartOfBookAdmin)
admin.site.register(BibliographicUnitPartOfPeriodical, BibliographicUnitPartOfPeriodicalAdmin)

