from django.db import models
from categories.models import Subcategory
from description_elements.models import Author, Translator, Location


class EncompassingBibliographicUnit(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author,
                                     related_name='encompassing_bibliographic_units',
                                     verbose_name='Autor/Autorzy')
    translators = models.ManyToManyField(Translator,
                                         related_name='encompassing_bibliographic_units',
                                         verbose_name='Tłumaczenie')
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    published_location = models.ManyToManyField(Location,
                                                related_name='encompassing_bibliographic_units',
                                                verbose_name='Miejsce/miejsca wydania')
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name="Tomy", blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name="Wydanie", blank=True, null=True)
    # TODO: ask what else can possible get here


class Periodical(models.Model):
    title = models.CharField(max_length=1000, verbose_name="Tytuł periodyku", blank=True, null=True)
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    vol_info_lvl_1 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 1", blank=True, null=True)
    vol_info_lvl_2 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 2", blank=True, null=True)
    vol_info_lvl_3 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 3", blank=True, null=True)


class BibliographicUnitBook(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bib_units_books', verbose_name='Autorstwo')
    translators = models.ManyToManyField(Translator, related_name='bib_units_books', verbose_name='Tłumaczenie')
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    published_location = models.ManyToManyField(Location,
                                                related_name='bib_units_books',
                                                verbose_name='Miejsce/miejsca wydania')
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name="Tomy", blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name="Wydanie", blank=True, null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_books',
                                                          verbose_name='Kategoria i podkategoria')
    # TODO: ask what else can possible get here ??

    class Meta:
        verbose_name = 'Opis (wydawnictwo zwarte)'
        verbose_name_plural = 'Opisy (wydawnictwa zwarte)'


class BibliographicUnitPartOfBook(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bib_units_parts_of_books', verbose_name='Autorstwo')
    translators = models.ManyToManyField(Translator, related_name='bib_units_parts_of_books', verbose_name='Tłumaczenie')
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    encompassing_bibliographic_unit_title = models.ForeignKey(EncompassingBibliographicUnit,
                                                              related_name='dependent_bibliographic_units',
                                                              verbose_name='Opublikowane w: (wydawnictwo zwarte)',
                                                              blank=True, null=True, on_delete=models.PROTECT)
    encompassing_bibliographic_unit_pages = models.CharField(max_length=100, verbose_name="Strony", blank=True,
                                                             null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_parts_of_books',
                                                          verbose_name='Kategoria i podkategoria')
    # TODO: ask what else can possible get here ??

    class Meta:
        verbose_name = 'Opis (część wydawnictwa zwartego)'
        verbose_name_plural = 'Opisy (części wydawnictw zwartych)'


class BibliographicUnitPartOfPeriodical(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bib_units_parts_of_periodicals', verbose_name='Autorstwo')
    translators = models.ManyToManyField(Translator, related_name='bib_units_parts_of_periodicals', verbose_name='Tłumaczenie')
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    periodical_title = models.ForeignKey(Periodical,
                                         related_name='contained_articles',
                                         verbose_name='Opublikowane w: (periodyk)',
                                         blank=True, null=True, on_delete=models.PROTECT)
    periodical_pages = models.CharField(max_length=100, verbose_name="Strony", blank=True, null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_parts_of_periodicals',
                                                          verbose_name='Kategoria i podkategoria')
    # TODO: ask what else can possible get here ??

    class Meta:
        verbose_name = 'Opis (w periodyku)'
        verbose_name_plural = 'Opisy (w periodykach)'
