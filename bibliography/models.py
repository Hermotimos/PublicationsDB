from django.db import models
from categories.models import Subcategory
from description_elements.models import Author, Translator, Location


class EncompassingBibliographicUnit(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author,
                                     related_name='encompassing_bibliographic_units',
                                     verbose_name='Autor/Autorzy',
                                     blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Czy więcej niż trzech autorów?', default=False)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='encompassing_bibliographic_units',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Czy więcej niż trzech tłumaczy?', default=False)

    edition = models.CharField(max_length=100, verbose_name='Wydanie', blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name='Tomy', blank=True, null=True)

    published_locations = models.ManyToManyField(Location,
                                                 related_name='encompassing_bibliographic_units',
                                                 verbose_name='Miejsce/miejsca wydania',
                                                 blank=True)
    published_year = models.CharField(max_length=100, verbose_name='Rok wydania', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)

    def save(self, *args, **kwargs):
        super(EncompassingBibliographicUnit, self).save(*args, **kwargs)
        self.sorting_name = self.__str__()
        super(EncompassingBibliographicUnit, self).save(*args, **kwargs)

    def __str__(self):
        if self.title and self.authors.all().count() > 0 and not self.authorship:
            title = f', {self.title}'
        elif self.title and self.authorship:
            title = self.title
        elif self.title and self.authors.all().count() == 0:
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

        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''

        if self.authorship:
            authorship = f', {self.authorship}'
            authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{title}{ed}{authorship}{authors}{et_alii_authors}{translators}{et_alii_translators}{vols}{locations}{year}'
        else:
            authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{authors}{et_alii_authors}{title}{ed}{translators}{et_alii_translators}{vols}{locations}{year}'

    class Meta:
        verbose_name = 'Wydawnictwo zwarte nadrzędne'
        verbose_name_plural = 'Wydawnictwa zwarte nadrzędne'
        ordering = ['sorting_name']


class Periodical(models.Model):
    title = models.CharField(max_length=1000, verbose_name='Tytuł periodyku', blank=True, null=True)
    published_year = models.CharField(max_length=100, verbose_name='Rok wydania', blank=True, null=True)
    vol_info_lvl_1 = models.CharField(max_length=100, verbose_name='Numeracja wolumenu poziom 1', blank=True, null=True)
    vol_info_lvl_2 = models.CharField(max_length=100, verbose_name='Numeracja wolumenu poziom 2', blank=True, null=True)
    vol_info_lvl_3 = models.CharField(max_length=100, verbose_name='Numeracja wolumenu poziom 3', blank=True, null=True)

    def __str__(self):
        title = self.title
        year = f' {self.published_year}' if self.published_year else ''
        lvl1 = f', {self.vol_info_lvl_1}' if self.vol_info_lvl_1 else ''
        lvl2 = f', {self.vol_info_lvl_2}' if self.vol_info_lvl_2 else ''
        lvl3 = f', {self.vol_info_lvl_3}' if self.vol_info_lvl_3 else ''
        return f'"{title}"{year}{lvl1}{lvl2}{lvl3}'

    class Meta:
        verbose_name = 'Periodyk'
        verbose_name_plural = 'Periodyki'


class BibliographicUnitBook(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bib_units_books', verbose_name='Autorstwo', blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Czy więcej niż trzech autorów?', default=False)
    translators = models.ManyToManyField(Translator, related_name='bib_units_books', verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Czy więcej niż trzech tłumaczy?', default=False)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)

    published_locations = models.ManyToManyField(Location,
                                                 related_name='bib_units_books',
                                                 verbose_name='Miejsce/miejsca wydania',
                                                 blank=True)
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name='Tomy (np. "t. 1-2")', blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name='Wydanie', blank=True, null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_books',
                                                          verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name='Uwagi', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)

    def __str__(self):
        if self.title and self.authors.all().count() > 0 and not self.authorship:
            title = f', {self.title}'
        elif self.title and self.authorship:
            title = self.title
        elif self.title and self.authors.all().count() == 0:
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

        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''
        annotation = f' [{self.annotation}]' if self.annotation else ''

        if self.authorship:
            authorship = f', {self.authorship}'
            authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{title}{ed}{authorship}{authors}{et_alii_authors}{translators}{et_alii_translators}{vols}{locations}{year}.{annotation}'
        else:
            authors = ', '.join(f' {a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{authors}{et_alii_authors}{title}{ed}{translators}{et_alii_translators}{vols}{locations}{year}.{annotation}'

    def save(self, *args, **kwargs):
        super(BibliographicUnitBook, self).save(*args, **kwargs)
        self.sorting_name = self.__str__()
        super(BibliographicUnitBook, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '1. Opis bibliograficzny (wydawnictwo zwarte)'
        verbose_name_plural = '1. Opisy bibliograficzne (wydawnictwa zwarte)'
        ordering = ['sorting_name']


class BibliographicUnitPartOfBook(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_books',
                                     verbose_name='Autorstwo',
                                     blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Czy więcej niż trzech autorów?', default=False)
    translators = models.ManyToManyField(Translator,
                                         related_name='bib_units_parts_of_books',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Czy więcej niż trzech tłumaczy?', default=False)
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    encompassing_bibliographic_unit = models.ForeignKey(EncompassingBibliographicUnit,
                                                        related_name='dependent_bibliographic_units',
                                                        verbose_name='Opublikowane w: (wydawnictwo zwarte)',
                                                        on_delete=models.PROTECT)
    in_volume = models.CharField(max_length=100, verbose_name='Tom (np. "t. 2")', blank=True, null=True)
    encompassing_bibliographic_unit_pages = models.CharField(max_length=100, verbose_name='Strony (np. "str. 7-77")',
                                                             blank=True, null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_parts_of_books',
                                                          verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name='Uwagi', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)

    def __str__(self):
        # PART 1: elements considering bibliographic unit being part of a book:
        if self.title and self.authors.all().count() > 0 and not self.authorship:
            title = f', {self.title}'
        elif self.title and self.authorship:
            title = self.title
        elif self.title and self.authors.all().count() == 0:
            title = self.title
        else:
            title = '[n/a]'

        translators = f', tłum. {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''
        vol = f', {self.in_volume}' if self.in_volume else ''
        pages = f', {self.encompassing_bibliographic_unit_pages}' if self.encompassing_bibliographic_unit_pages else ''

        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''
        annotation = f' [{self.annotation}]' if self.annotation else ''

        # PART 2: elements considering encompassing bibliographic unit:
        unit = self.encompassing_bibliographic_unit

        if unit.title and unit.authors.all().count() > 0 and not unit.authorship:
            u_title = f', {unit.title}'
        elif unit.title and unit.authorship:
            u_title = unit.title
        elif unit.title and unit.authors.all().count() == 0:
            u_title = unit.title
        else:
            u_title = '[n/a]'

        u_ed = f', {unit.edition}' if unit.edition else ''
        u_translators = f', tłum. {", ".join(str(t) for t in unit.translators.all())}' if unit.translators.all() else ''
        if unit.published_locations.all().count() == 1:
            u_locations = f', {unit.published_locations.first()}'
        elif unit.published_locations.all().count() > 1:
            u_locations = f', {"-".join(str(l) for l in unit.published_locations.all())}'
        else:
            u_locations = ''

        if unit.published_year and (unit.published_locations.all().count() >= 1):
            u_year = f' {unit.published_year}'
        elif unit.published_year and unit.published_locations.all().count() == 0:
            u_year = f', {unit.published_year}'
        else:
            u_year = '[n/a]'

        u_et_alii_authors = ' i in.' if unit.is_over_three_authors else ''
        u_et_alii_translators = ' i in.' if unit.is_over_three_translators else ''

        if unit.authorship:
            u_authorship = f', {unit.authorship}'
            u_authors = ', '.join(
                f' {a.first_names} {a.last_name}' for a in unit.authors.all()) if unit.authors.all() else ''
            unit = f', w: {u_title}{u_ed}{u_authorship}{u_authors}{u_et_alii_authors}{u_translators}{u_et_alii_translators}{vol}{u_locations}{u_year}'
        else:
            u_authors = ', '.join(
                f' {a.first_names} {a.last_name}' for a in unit.authors.all()) if unit.authors.all() else ''
            unit = f', w: {u_authors}{u_et_alii_authors}{u_title}{u_ed}{u_translators}{u_et_alii_translators}{vol}{u_locations}{u_year}'

        # PART 3: return constructs the bibliographic description:
        if self.authorship:
            authorship = f', {self.authorship}'
            authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{title}{authorship}{authors}{et_alii_authors}{translators}{et_alii_translators}{unit}{pages}.{annotation}'
        else:
            authors = ', '.join(f' {a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{authors}{et_alii_authors}{title}{translators}{et_alii_translators}{unit}{pages}.{annotation}'

    def save(self, *args, **kwargs):
        super(BibliographicUnitPartOfBook, self).save(*args, **kwargs)
        self.sorting_name = self.__str__()
        super(BibliographicUnitPartOfBook, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '2. Opis bibliograficzny (w ramach wydawnictwa zwartego)'
        verbose_name_plural = '2. Opisy bibliograficzne (w ramach wydawnictw zwartych)'
        ordering = ['sorting_name']


class BibliographicUnitPartOfPeriodical(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red.)', blank=True, null=True)
    authors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_periodicals',
                                     verbose_name='Autorstwo',
                                     blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Czy więcej niż trzech autorów?', default=False)
    translators = models.ManyToManyField(Translator,
                                         related_name='bib_units_parts_of_periodicals',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Czy więcej niż trzech tłumaczy?', default=False)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)

    periodical = models.ForeignKey(Periodical,
                                         related_name='contained_articles',
                                         verbose_name='Opublikowane w: (periodyk)',
                                         on_delete=models.PROTECT)
    periodical_pages = models.CharField(max_length=100, verbose_name='Strony (np. "str. 7-77")', blank=True, null=True)

    categories_and_subcategories = models.ManyToManyField(Subcategory,
                                                          related_name='bib_units_parts_of_periodicals',
                                                          verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name='Uwagi', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)

    def __str__(self):
        # PART 1: elements considering bibliographic unit being part of a periodical:
        if self.title and self.authors.all().count() > 0 and not self.authorship:
            title = f', {self.title}'
        elif self.title and self.authorship:
            title = self.title
        elif self.title and self.authors.all().count() == 0:
            title = self.title
        else:
            title = '[n/a]'

        translators = f', tłum. {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''
        pages = f', {self.periodical_pages}' if self.periodical_pages else ''

        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''
        annotation = f' [{self.annotation}]' if self.annotation else ''

        # PART 2: elements considering the periodical:
        periodical = f', {self.periodical}'

        # PART 3: return constructs the bibliographic description:
        if self.authorship:
            authorship = f', {self.authorship}'
            authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{title}{authorship}{authors}{et_alii_authors}{translators}{et_alii_translators}{periodical}{pages}.{annotation}'
        else:
            authors = ', '.join(f' {a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
            return f'{authors}{et_alii_authors}{title}{translators}{et_alii_translators}{periodical}{pages}.{annotation}'

    def save(self, *args, **kwargs):
        super(BibliographicUnitPartOfPeriodical, self).save(*args, **kwargs)
        self.sorting_name = self.__str__()
        super(BibliographicUnitPartOfPeriodical, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '3. Opis bibliograficzny (w periodyku)'
        verbose_name_plural = '3. Opisy bibliograficzne (w periodykach)'
