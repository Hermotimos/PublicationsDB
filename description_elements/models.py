from django.db import models


class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Autor/Redaktor'
        verbose_name_plural = 'Autorzy i redaktorzy'
        ordering = ['last_name', ]

    def __str__(self):
        return f'{self.last_name} {self.first_names}' if self.first_names else self.last_name


class Translator(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Tłumacz'
        verbose_name_plural = 'Tłumacze'
        ordering = ['last_name', ]

    def __str__(self):
        return f'{self.first_names} {self.last_name}'


class Location(models.Model):
    name = models.CharField(max_length=500, verbose_name="Miejscowość")

    class Meta:
        verbose_name = 'Miejscowość'
        verbose_name_plural = 'Miejscowości'
        ordering = ['name', ]

    def __str__(self):
        return self.name





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

class EncompassingBibliographicUnit(models.Model):
    authors = models.ManyToManyField(Author,
                                     related_name='encompassing_bib_units_as_author',
                                     verbose_name='Autorstwo',
                                     blank=True)
    is_over_three_authors = models.BooleanField(verbose_name='Więcej niż trzech autorów?', default=False)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)
    editorship = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
                                  blank=True, null=True)
    editors = models.ManyToManyField(Author,
                                     related_name='encompassing_bib_units_as_editor',
                                     verbose_name='Redakcja/Opracowanie itp.',
                                     blank=True)
    is_over_three_editors = models.BooleanField(verbose_name='Więcej niż trzech red./oprac. itp.?', default=False)
    translators = models.ManyToManyField(Translator,
                                         related_name='encompassing_bib_units_as_translator',
                                         verbose_name='Tłumaczenie',
                                         blank=True)
    is_over_three_translators = models.BooleanField(verbose_name='Więcej niż trzech tłumaczy?', default=False)

    edition = models.CharField(max_length=100, verbose_name='Wydanie', blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name='Tomy', blank=True, null=True)
    published_locations = models.ManyToManyField(Location,
                                                 related_name='encompassing_bib_units',
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
        authors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.authors.all()) if self.authors.all() else ''
        editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        translators = f', tłum. {", ".join(str(t) for t in self.translators.all())}' if self.translators.all() else ''

        editorship = f', {self.editorship}' if self.editorship else ''
        et_alii_authors = ' i in.' if self.is_over_three_authors else ''
        et_alii_editors = ' i in.' if self.is_over_three_editors else ''
        et_alii_translators = ' i in.' if self.is_over_three_translators else ''

        if self.title and self.authors.all().count() > 0:
            title = f', {self.title}'
        else:
            title = self.title

        ed = f', {self.edition}' if self.edition else ''
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
        elif not self.published_locations and self.published_locations.all().count() == 0:
            year = ', [brw]'
        else:
            ' [błąd instrukcji warunkowej!]'

        return f'{authors}{et_alii_authors}{title}{ed}{editorship}{editors}{et_alii_editors}{translators}{et_alii_translators}{vols}{locations}{year}'

    class Meta:
        verbose_name = 'Wydawnictwo zwarte nadrzędne'
        verbose_name_plural = 'Wydawnictwa zwarte nadrzędne'
        ordering = ['sorting_name']