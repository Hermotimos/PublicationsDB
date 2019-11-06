from django.db import models
from django.utils.html import format_html
from publications_db.utils import replace_special_chars, remove_tags


class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = '1. Autor/Redaktor'
        verbose_name_plural = '1. Autorzy i redaktorzy'
        ordering = ['last_name', ]
        unique_together = ['first_names', 'last_name']

    def __str__(self):
        return f'{self.last_name} {self.first_names}' if self.first_names else self.last_name


class Translator(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = '2. Tłumacz'
        verbose_name_plural = '2. Tłumacze'
        ordering = ['last_name', ]
        unique_together = ['first_names', 'last_name']

    def __str__(self):
        return f'{self.last_name} {self.first_names}'


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Miejscowość", unique=True)

    class Meta:
        verbose_name = '3. Miejscowość'
        verbose_name_plural = '3. Miejscowości'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Periodical(models.Model):
    title = models.CharField(max_length=1000, verbose_name='Tytuł periodyku', blank=True, null=True)
    published_year = models.CharField(max_length=20, verbose_name='Rok wydania', blank=True, null=True)
    vol_info_lvl_1 = models.CharField(max_length=30, verbose_name='Numeracja wolumenu poziom 1', blank=True, null=True)
    vol_info_lvl_2 = models.CharField(max_length=30, verbose_name='Numeracja wolumenu poziom 2', blank=True, null=True)
    vol_info_lvl_3 = models.CharField(max_length=30, verbose_name='Numeracja wolumenu poziom 3', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)

    def __str__(self):
        title = self.title
        year = f' {self.published_year}' if self.published_year else ''
        lvl1 = f', {self.vol_info_lvl_1}' if self.vol_info_lvl_1 else ''
        lvl2 = f', {self.vol_info_lvl_2}' if self.vol_info_lvl_2 else ''
        lvl3 = f', {self.vol_info_lvl_3}' if self.vol_info_lvl_3 else ''
        return f'„{title}”{year}{lvl1}{lvl2}{lvl3}'

    def save(self, *args, **kwargs):
        super(Periodical, self).save(*args, **kwargs)
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        super(Periodical, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '4. Periodyk'
        verbose_name_plural = '4. Periodyki'
        unique_together = ['title', 'published_year', 'vol_info_lvl_1', 'vol_info_lvl_2', 'vol_info_lvl_3']
        ordering = ['sorting_name']


class EncompassingBibliographicUnit(models.Model):
    authors = models.ManyToManyField(Author,
                                     related_name='encompassing_bib_units_as_author',
                                     verbose_name='Autorstwo',
                                     blank=True)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)
    editors_abbrev = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
                                      blank=True, null=True)
    editors = models.ManyToManyField(Author,
                                     related_name='encompassing_bib_units_as_editor',
                                     verbose_name='Redakcja/Opracowanie itp.',
                                     blank=True)
    translators_abbrev = models.CharField(max_length=100, verbose_name='Skrót tłumaczenia (np. tłum.)',
                                          blank=True, null=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='encompassing_bib_units_as_translator',
                                         verbose_name='Tłumaczenie',
                                         blank=True)

    # edition = models.CharField(max_length=100, verbose_name='Wydanie', blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name='Tomy', blank=True, null=True)
    published_locations = models.ManyToManyField(Location,
                                                 related_name='encompassing_bib_units',
                                                 verbose_name='Miejsce/miejsca wydania',
                                                 blank=True)
    published_year = models.CharField(max_length=100, verbose_name='Rok wydania', blank=True, null=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)

    def __str__(self):
        authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
        editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        translators = f', {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''

        editors_abbrev = f', {self.editors_abbrev}' if self.editors_abbrev else ''

        if self.title and self.authors.all().count() > 0:
            title = f', {self.title}'
        else:
            title = self.title

        # ed = f', {self.edition}' if self.edition else ''
        vols = f', {self.volumes}' if self.volumes else ''

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
            year = ', [b.m.], [b.r.]'
        else:
            year = ' [błąd instrukcji warunkowej!]'

        description = f'{authors}' \
            f'<i>{title}</i>' \
            f'{editors_abbrev}{editors}' \
            f'{translators}' \
            f'{vols}{locations}{year}'

        return format_html(f'{description}')

    def save(self, *args, **kwargs):
        super(EncompassingBibliographicUnit, self).save(*args, **kwargs)
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        super(EncompassingBibliographicUnit, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '5. Wydawnictwo zwarte nadrzędne'
        verbose_name_plural = '5. Wydawnictwa zwarte nadrzędne'
        ordering = ['sorting_name']
