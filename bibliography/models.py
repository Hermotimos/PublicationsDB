from django.db import models
from django.utils.html import format_html
from categories.models import CategoryLevelThree
from description_elements.models import Author, Translator, Location, EncompassingBibliographicUnit, Periodical
from publications_db.utils import replace_special_chars


class BibliographicUnitBook(models.Model):
    authors = models.ManyToManyField(Author,
                                     related_name='bib_units_books_as_author',
                                     verbose_name='Autorstwo',
                                     blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Więcej niż trzech autorów?', default=False)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)
    editors_abbrev = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
                                      blank=True, null=True)
    editors = models.ManyToManyField(Author,
                                     related_name='bib_units_books_as_editor',
                                     verbose_name='Redakcja/Opracowanie itp.',
                                     blank=True)
    is_over_three_editors = models.BooleanField(verbose_name='Więcej niż trzech red./oprac. itp.?', default=False)
    translators_abbrev = models.CharField(max_length=100, verbose_name='Skrót tłumaczenia (np. tłum.)',
                                          blank=True, null=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='bib_units_books_as_translator',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Więcej niż trzech tłumaczy?', default=False)

    published_locations = models.ManyToManyField(Location,
                                                 related_name='bib_units_books',
                                                 verbose_name='Miejsce/miejsca wydania',
                                                 blank=True)
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name='Tomy (np. "t. 1-2")', blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name='Wydanie', blank=True, null=True)

    cat_lvl_3 = models.ManyToManyField(CategoryLevelThree,
                                       related_name='bib_units_books',
                                       verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name='Uwagi', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (pole wypełniane automatycznie)',
                                    blank=True, null=True)
    description = models.CharField(max_length=1000, verbose_name='Opis bibliograficzny (pole wypełniane automatycznie)',
                                   blank=True, null=True)

    def __str__(self):
        authors = ', '.join(f' {a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
        editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        translators = f' {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''

        editors_abbrev = f', {self.editors_abbrev}' if self.editors_abbrev else ''
        translators_abbrev = f', {self.translators_abbrev}' if self.translators_abbrev else ''
        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_editors = ' i in.' if self.is_over_three_editors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''

        if self.title and self.authors.all().count() > 0:
            title = f', {self.title}'
        else:
            title = self.title

        ed = f', {self.edition}' if self.edition else ''
        vols = f', {self.volumes}' if self.volumes else ''
        annotation = f' [{self.annotation}]' if self.annotation else ''

        if self.published_locations.all().count() == 1:
            locations = f', {self.published_locations.first()}'
        elif self.published_locations.all().count() > 1:
            locations = f', {"-".join(str(l) for l in self.published_locations.all())}'
        else:
            locations = ''

        if self.published_year and self.published_locations.all().count() >= 1:
            year = f' {self.published_year}'
        elif self.published_year and self.published_locations.all().count() == 0:
            year = f', {self.published_year}'
        elif not self.published_year and self.published_locations.all().count() >= 1:
            year = ' [brw]'
        elif not self.published_year and self.published_locations.all().count() == 0:
            year = ', [bmw brw]'
        else:
            year = ' [błąd instrukcji warunkowej!]'

        description = f'{authors}{et_alii_authors}' \
            f'<i>{title}</i>' \
            f'{ed}{editors_abbrev}{editors}{et_alii_editors}' \
            f'{translators_abbrev}{translators}{et_alii_translators}' \
            f'{vols}{locations}{year}.{annotation}'

        return format_html(f'{description}')

    def save(self, *args, **kwargs):
        super(BibliographicUnitBook, self).save(*args, **kwargs)
        self.description = self.__str__()
        self.sorting_name = replace_special_chars(self.__str__())
        super(BibliographicUnitBook, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '1. Wydawnictwo zwarte'
        verbose_name_plural = '1. Wydawnictwa zwarte'
        ordering = ['sorting_name']


class BibliographicUnitPartOfBook(models.Model):
    authors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_books_as_author',
                                     verbose_name='Autorstwo',
                                     blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Więcej niż trzech autorów?', default=False)
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)
    editors_abbrev = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
                                      blank=True, null=True)
    editors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_books_as_editor',
                                     verbose_name='Redakcja/Opracowanie itp.',
                                     blank=True)
    is_over_three_editors = models.BooleanField(verbose_name='Więcej niż trzech red./oprac. itp.?', default=False)
    translators_abbrev = models.CharField(max_length=100, verbose_name='Skrót tłumaczenia (np. tłum.)',
                                          blank=True, null=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='bib_units_parts_of_books_as_translator',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Więcej niż trzech tłumaczy?', default=False)

    encompassing_bibliographic_unit = models.ForeignKey(EncompassingBibliographicUnit,
                                                        related_name='dependent_bibliographic_units',
                                                        verbose_name='Opublikowane w: (wydawnictwo zwarte)',
                                                        on_delete=models.PROTECT)
    in_volume = models.CharField(max_length=100, verbose_name='Tom (np. "t. 2")', blank=True, null=True)
    encompassing_bibliographic_unit_pages = models.CharField(max_length=100, verbose_name='Strony (np. "str. 7-77")',
                                                             blank=True, null=True)

    cat_lvl_3 = models.ManyToManyField(CategoryLevelThree,
                                       related_name='bib_units_parts_of_books',
                                       verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name='Uwagi', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)
    description = models.CharField(max_length=1000, verbose_name='Opis bibliograficzny (pole wypełniane automatycznie)',
                                   blank=True, null=True)

    def __str__(self):
        # PART 1: elements considering bibliographic unit being part of a book:
        authors = ', '.join(f' {a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
        editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        translators = f' {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''

        editors_abbrev = f', {self.editors_abbrev}' if self.editors_abbrev else ''
        translators_abbrev = f', {self.translators_abbrev}' if self.translators_abbrev else ''
        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_editors = ' i in.' if self.is_over_three_editors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''

        if self.title and self.authors.all().count() > 0:
            title = f', {self.title}'
        else:
            title = self.title

        vol = f', {self.in_volume}' if self.in_volume else ''
        pages = f', {self.encompassing_bibliographic_unit_pages}' if self.encompassing_bibliographic_unit_pages else ''
        annotation = f' [{self.annotation}]' if self.annotation else ''

        # PART 2: elements considering encompassing bibliographic unit:
        unit = self.encompassing_bibliographic_unit
        u_authors = ', '.join(f' {a.first_names} {a.last_name}' for a in unit.authors.all()) if unit.authors.all() else ''
        u_translators = f' {", ".join(str(t) for t in unit.translators.all())}' if unit.translators.all() else ''
        u_editors = ', '.join(f' {a.first_names} {a.last_name}' for a in unit.editors.all()) if unit.editors.all() else ''

        u_editors_abbrev = f', {unit.editors_abbrev}' if unit.editors_abbrev else ''
        u_translators_abbrev = f', {unit.translators_abbrev}' if unit.translators_abbrev else ''
        u_et_alii_editors = ' i in.' if unit.is_over_three_editors else ''
        u_et_alii_authors = ' i in.' if unit.is_over_three_authors else ''
        u_et_alii_translators = ' i in.' if unit.is_over_three_translators else ''

        if unit.title and unit.authors.all().count() > 0:
            u_title = f', {unit.title}'
        else:
            u_title = unit.title

        u_ed = f', {unit.edition}' if unit.edition else ''

        if unit.published_locations.all().count() == 1:
            u_locations = f', {unit.published_locations.first()}'
        elif unit.published_locations.all().count() > 1:
            u_locations = f', {"-".join(str(l) for l in unit.published_locations.all())}'
        else:
            u_locations = ''

        if unit.published_year and unit.published_locations.all().count() >= 1:
            u_year = f' {unit.published_year}'
        elif unit.published_year and unit.published_locations.all().count() == 0:
            u_year = f', {unit.published_year}'
        elif not unit.published_year and unit.published_locations.all().count() >= 1:
            u_year = ' [brw]'
        elif not unit.published_locations and unit.published_locations.all().count() == 0:
            u_year = ', [brw]'
        else:
            u_year = ' [błąd instrukcji warunkowej!]'

        unit = f', w: {u_authors}{u_et_alii_authors}' \
            f'{u_title}' \
            f'{u_ed}{u_editors_abbrev}{u_editors}{u_et_alii_editors}' \
            f'{u_translators_abbrev}{u_translators}{u_et_alii_translators}' \
            f'{vol}{u_locations}{u_year}'

        description = f'{authors}{et_alii_authors}' \
            f'<i>{title}</i>' \
            f'{editors_abbrev}{editors}{et_alii_editors}' \
            f'{translators_abbrev}{translators}{et_alii_translators}' \
            f'{unit}{pages}.{annotation}'

        return format_html(f'{description}')

    def save(self, *args, **kwargs):
        super(BibliographicUnitPartOfBook, self).save(*args, **kwargs)
        self.description = self.__str__()
        self.sorting_name = replace_special_chars(self.__str__())
        super(BibliographicUnitPartOfBook, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '2. Rozdział/artykuł/hasło itp. w wydawnictwie zwartym'
        verbose_name_plural = '2. Rozdziały/artykuły/hasła itp. w wydawnictwach zwartych'
        ordering = ['sorting_name']


class BibliographicUnitPartOfPeriodical(models.Model):
    authors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_periodicals_as_author',
                                     verbose_name='Autorstwo',
                                     blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Więcej niż trzech autorów?', default=False)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)
    editors_abbrev = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
                                      blank=True, null=True)
    editors = models.ManyToManyField(Author,
                                     related_name='bib_units_parts_of_periodicals_as_editor',
                                     verbose_name='Redakcja/Opracowanie itp.',
                                     blank=True)
    is_over_three_editors = models.BooleanField(verbose_name='Więcej niż trzech red./oprac. itp.?', default=False)
    translators_abbrev = models.CharField(max_length=100, verbose_name='Skrót tłumaczenia (np. tłum.)',
                                          blank=True, null=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='bib_units_parts_of_periodicals_as_translator',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Więcej niż trzech tłumaczy?', default=False)

    periodical = models.ForeignKey(Periodical,
                                   related_name='contained_articles',
                                   verbose_name='Opublikowane w: (periodyk)',
                                   on_delete=models.PROTECT)
    periodical_pages = models.CharField(max_length=100, verbose_name='Strony (np. "str. 7-77")', blank=True, null=True)

    cat_lvl_3 = models.ManyToManyField(CategoryLevelThree,
                                       related_name='bib_units_parts_of_periodicals',
                                       verbose_name='Kategoria i podkategoria')
    annotation = models.CharField(max_length=1000, verbose_name='Uwagi', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)
    description = models.CharField(max_length=1000, verbose_name='Opis bibliograficzny (pole wypełniane automatycznie)',
                                   blank=True, null=True)

    def __str__(self):
        # PART 1: elements considering bibliographic unit being part of a periodical:
        authors = ', '.join(f' {a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
        editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        translators = f' {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''

        editors_abbrev = f', {self.editors_abbrev}' if self.editors_abbrev else ''
        translators_abbrev = f', {self.translators_abbrev}' if self.translators_abbrev else ''
        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_editors = ' i in.' if self.is_over_three_editors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''

        if self.title and self.authors.all().count() > 0:
            title = f', {self.title}'
        else:
            title = self.title

        pages = f', {self.periodical_pages}' if self.periodical_pages else ''
        annotation = f' [{self.annotation}]' if self.annotation else ''

        # PART 2: elements considering the periodical:
        periodical = f', {self.periodical}'

        description = f'{authors}{et_alii_authors}' \
            f'<i>{title}</i>' \
            f'{editors_abbrev}{editors}{et_alii_editors}' \
            f'{translators_abbrev}{translators}{et_alii_translators}' \
            f'{periodical}{pages}.{annotation}'

        return format_html(f'{description}')

    def save(self, *args, **kwargs):
        super(BibliographicUnitPartOfPeriodical, self).save(*args, **kwargs)
        self.description = self.__str__()
        self.sorting_name = replace_special_chars(self.__str__())
        super(BibliographicUnitPartOfPeriodical, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '3. Artykuł w periodyku'
        verbose_name_plural = '3. Artykuły w periodykach'
        ordering = ['sorting_name']
