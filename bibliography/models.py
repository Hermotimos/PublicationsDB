from django.db import models
from categories.models import Subcategory
from description_elements.models import Author, Translator, Location


class EncompassingBibliographicUnit(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author,
                                     related_name='encompassing_bibliographic_units',
                                     verbose_name='Autor/Autorzy',
                                     blank=True)
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='encompassing_bibliographic_units',
                                         verbose_name='Tłumaczenie',
                                         blank=True)

    edition = models.CharField(max_length=100, verbose_name="Wydanie", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name="Tomy", blank=True, null=True)

    published_locations = models.ManyToManyField(Location,
                                                 related_name='encompassing_bibliographic_units',
                                                 verbose_name='Miejsce/miejsca wydania',
                                                 blank=True)
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)

    def __str__(self):
        if self.title and self.authors and not self.authorship:
            title = f', {self.title}'
        elif self.title and self.authorship:
            title = self.title
        elif self.title and not self.authors:
            title = self.title
        else:
            title = '[n/a]'

        ed = f', {self.edition}' if self.edition else ''
        translators = f', tłum. {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''
        vols = f', {self.volumes}' if self.volumes else ''
        if self.published_locations.all().count() == 1:
            locations = f', {self.published_locations.first()}'
        elif self.published_locations.all().count() > 1:
            locations = f', {"-".join(str(l) for l in self.published_locations.all())}'
        else:
            locations = ''

        if self.published_year and (self.published_locations.all().count() >= 1):
            year = f' {self.published_year}'
        elif self.published_year and self.published_locations.all().count() == 0:
            year = f', {self.published_year}'
        else:
            year = '[n/a]'

        if self.authorship:
            authorship = f', {self.authorship}'
            authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{title}{ed}{authorship}{authors}{translators}{vols}{locations}{year}'
        else:
            authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{authors}{title}{ed}{translators}{vols}{locations}{year}'

    class Meta:
        verbose_name = 'Wydawnictwo zwarte (nadrzędne)'
        verbose_name_plural = 'Wydawnictwa zwarte (nadrzędne)'


class Periodical(models.Model):
    title = models.CharField(max_length=1000, verbose_name="Tytuł periodyku", blank=True, null=True)
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    vol_info_lvl_1 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 1", blank=True, null=True)
    vol_info_lvl_2 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 2", blank=True, null=True)
    vol_info_lvl_3 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 3", blank=True, null=True)

    def __str__(self):
        title = self.title
        year = f' {self.published_year}' if self.published_year else ''
        lvl1 = f', {self.vol_info_lvl_1}' if self.vol_info_lvl_1 else ''
        lvl2 = f', {self.vol_info_lvl_2}' if self.vol_info_lvl_2 else ''
        lvl3 = f', {self.vol_info_lvl_3}' if self.vol_info_lvl_3 else ''
        return f'"{title}"{year}{lvl1}{lvl2}{lvl3}, '

    class Meta:
        verbose_name = 'Periodyk'
        verbose_name_plural = 'Periodyki'


class BibliographicUnitBook(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bib_units_books', verbose_name='Autorstwo', blank=True)
    translators = models.ManyToManyField(Translator, related_name='bib_units_books', verbose_name='Tłumaczenie',
                                         blank=True)
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    published_locations = models.ManyToManyField(Location,
                                                 related_name='bib_units_books',
                                                 verbose_name='Miejsce/miejsca wydania',
                                                 blank=True)
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name="Tomy", blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name="Wydanie", blank=True, null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_books',
                                                          verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name="Uwagi", blank=True, null=True)

    class Meta:
        verbose_name = '1. Opis (wydawnictwo zwarte)'
        verbose_name_plural = '1. Opisy (wydawnictwa zwarte)'


class BibliographicUnitPartOfBook(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_books',
                                     verbose_name='Autorstwo',
                                     blank=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='bib_units_parts_of_books',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)
    in_volume = models.CharField(max_length=100, verbose_name="W tomie", blank=True, null=True)

    encompassing_bibliographic_unit_title = models.ForeignKey(EncompassingBibliographicUnit,
                                                              related_name='dependent_bibliographic_units',
                                                              verbose_name='Opublikowane w: (wydawnictwo zwarte)',
                                                              on_delete=models.PROTECT)
    encompassing_bibliographic_unit_pages = models.CharField(max_length=100, verbose_name="Strony", blank=True,
                                                             null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_parts_of_books',
                                                          verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name="Uwagi", blank=True, null=True)

    class Meta:
        verbose_name = '2. Opis (część wydawnictwa zwartego)'
        verbose_name_plural = '2. Opisy (części wydawnictw zwartych)'


class BibliographicUnitPartOfPeriodical(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_periodicals',
                                     verbose_name='Autorstwo',
                                     blank=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='bib_units_parts_of_periodicals',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    periodical_title = models.ForeignKey(Periodical,
                                         related_name='contained_articles',
                                         verbose_name='Opublikowane w: (periodyk)',
                                         on_delete=models.PROTECT)
    periodical_pages = models.CharField(max_length=100, verbose_name="Strony", blank=True, null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_parts_of_periodicals',
                                                          verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name="Uwagi", blank=True, null=True)

    class Meta:
        verbose_name = '3. Opis (w periodyku)'
        verbose_name_plural = '3. Opisy (w periodykach)'
