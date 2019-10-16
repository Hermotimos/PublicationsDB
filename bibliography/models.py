from django.db import models


# TODO move Author and Location to another app in order to create division in admin !!!!

class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Inicjał/y')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'


class Translator(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Inicjał/y')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Tłumacz'
        verbose_name_plural = 'Tłumacze'


class Location(models.Model):
    name = models.CharField(max_length=500, verbose_name="Miejscowość")

    class Meta:
        verbose_name = 'Miejscowość'
        verbose_name_plural = 'Miejscowości'


class EncompassingBibliographicUnit(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red., oprac.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bibliographic_units', verbose_name='Autor/Autorzy')
    translators = models.ManyToManyField(Translator, related_name='bibliographic_units', verbose_name='Tłumaczenie')
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    published_location = models.ManyToManyField(Location, related_name='bibliographic_units', verbose_name='Miejsce/miejsca wydania')
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name="Tomy", blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name="Wydanie", blank=True, null=True)
    # TODO: ask what else can possible get here


class Periodical(models.Model):
    title = models.CharField(max_length=1000, verbose_name="Tytuł periodyku", blank=True, null=True)
    published_year = models.CharField(max_length=100, verbose_name="Rocznik", blank=True, null=True)
    volume_info_lvl_1 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 1", blank=True, null=True)  # TODO make verbose_names more precise - consult client
    volume_info_lvl_2 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 2", blank=True, null=True)  # TODO make verbose_names more precise - consult client
    volume_info_lvl_3 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 3", blank=True, null=True)  # TODO make verbose_names more precise - consult client


class BibliographicUnit(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red., oprac.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bibliographic_units', verbose_name='Autorstwo')
    translators = models.ManyToManyField(Translator, related_name='bibliographic_units', verbose_name='Tłumaczenie')
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    # case A: independent bibliographic unit:
    published_location = models.ManyToManyField(Location, related_name='bibliographic_units', verbose_name='Miejsce/miejsca wydania')
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name="Tomy", blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name="Wydanie", blank=True, null=True)
    # TODO: ask what else can possible get here ??

    # case B: published within another, independent bibliograhic unit:
    encompassing_bibliographic_unit_title = models.ManyToManyField(EncompassingBibliographicUnit, related_name='dependent_bibliographic_units', verbose_name='Opublikowane w: (wydawnictwo zwarte)')
    encompassing_bibliographic_unit_pages = models.CharField(max_length=100, verbose_name="Strony", blank=True, null=True)

    # case C: published within a periodical bibliographic unit:
    periodical_title = models.ManyToManyField(Periodical, related_name='contained_articles', verbose_name='Opublikowane w: (periodyk)')
    periodical_pages = models.CharField(max_length=100, verbose_name="Strony", blank=True, null=True)

    # Fields to add in future:
    # category_and_subcategory = models.ManyToManyField
    # they have to be listed together: 'Ludzie KUL/Wielcy kanclerze', 'Ludzie KUL/Rektorzy', 'Ludzie KUL/Prorektorzy' etc.

    class Meta:
        verbose_name = 'Opis bibliograficzny'
        verbose_name_plural = 'Opisy bibliograficzne'

