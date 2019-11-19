from django.db import models
from django.db.models.signals import m2m_changed
from django.utils.html import format_html

from publications_db.utils import replace_special_chars, remove_tags


class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_names}' if self.first_names else self.last_name

    def save(self, *args, **kwargs):
        super(Author, self).save(*args, **kwargs)
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        super(Author, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '1. Autor/Redaktor'
        verbose_name_plural = '1. Autorzy i redaktorzy'
        ordering = ['sorting_name']
        unique_together = ['first_names', 'last_name']


class Translator(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_names}'

    def save(self, *args, **kwargs):
        super(Translator, self).save(*args, **kwargs)
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        super(Translator, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '2. Tłumacz'
        verbose_name_plural = '2. Tłumacze'
        ordering = ['sorting_name']
        unique_together = ['first_names', 'last_name']


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Miejscowość", unique=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '3. Miejscowość'
        verbose_name_plural = '3. Miejscowości'
        ordering = ['sorting_name']


class Keyword(models.Model):
    name = models.CharField(max_length=100, verbose_name='Wyrażenie kluczowe', unique=True)
    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Keyword, self).save(*args, **kwargs)
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        super(Keyword, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '4. Wyrażenie kluczowe'
        verbose_name_plural = '4. Wyrażenia kluczowe'
        ordering = ['sorting_name']


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
        verbose_name = '5. Periodyk'
        verbose_name_plural = '5. Periodyki'
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
    # volumes = models.CharField(max_length=100, verbose_name='Tomy', blank=True, null=True)
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
        # vols = f', {self.volumes}' if self.volumes else ''

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
            f'{locations}{year}'

        return format_html(f'{description}')

    class Meta:
        verbose_name = '6. Wydawnictwo zwarte nadrzędne'
        verbose_name_plural = '6. Wydawnictwa zwarte nadrzędne'
        ordering = ['sorting_name']


def save_again(sender, instance, **kwargs):
    """Saves sender instance again to populate fields based on m2m fields of the same model"""
    instance.sorting_name = replace_special_chars(remove_tags(instance.__str__()))
    instance.save()


m2m_changed.connect(save_again, sender=EncompassingBibliographicUnit.authors.through)
m2m_changed.connect(save_again, sender=EncompassingBibliographicUnit.editors.through)
m2m_changed.connect(save_again, sender=EncompassingBibliographicUnit.translators.through)
m2m_changed.connect(save_again, sender=EncompassingBibliographicUnit.published_locations.through)
