from django.db import models
from django.db.models.signals import m2m_changed
from django.utils.html import format_html

from categories.models import CategoryLevelThree
from description_elements.models import Author, Translator, Location, Keyword, EncompassingBibliographicUnit, Periodical
from publications_db.utils import replace_special_chars, remove_tags


class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name='books_as_author', verbose_name='Autorstwo', blank=True)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)
    editors_abbrev = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
                                      blank=True, null=True)
    editors = models.ManyToManyField(Author,
                                     related_name='books_as_editor',
                                     verbose_name='Redakcja/Opracowanie itp.',
                                     blank=True)
    translators_abbrev = models.CharField(max_length=100, verbose_name='Skrót tłumaczenia (np. tłum.)',
                                          blank=True, null=True)
    translators = models.ManyToManyField(Translator,
                                         related_name='books_as_translator',
                                         verbose_name='Tłumaczenie',
                                         blank=True)

    published_locations = models.ManyToManyField(Location,
                                                 related_name='books',
                                                 verbose_name='Miejsce/miejsca wydania',
                                                 blank=True)
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name='Tomy (np. "t. 1-2")', blank=True, null=True)
    # edition = models.CharField(max_length=100, verbose_name='Wydanie', blank=True, null=True)

    cat_lvl_3 = models.ManyToManyField(CategoryLevelThree,
                                       related_name='books',
                                       verbose_name='Kategorie i podkategorie')
    annotation = models.CharField(max_length=10000, verbose_name='Uwagi', blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, related_name='books', verbose_name='Wyrażenia kluczowe', blank=True)

    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)
    description = models.CharField(max_length=1000, verbose_name='Opis bibliograficzny (pole automatyczne)',
                                   blank=True, null=True)

    def __str__(self):
        authors = ', '.join(f'{a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
        editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        translators = ', '.join(f' {a.first_names} {a.last_name}' for a in self.translators.all()) if self.translators.all() else ''

        editors_abbrev = f', {self.editors_abbrev}' if self.editors_abbrev else ''
        translators_abbrev = f', {self.translators_abbrev}' if self.translators_abbrev else ''

        if self.title and self.authors.all().count() > 0:
            title = f', <i>{self.title}</i>'
        elif not self.title:
            title = ', '
        else:
            title = f'<i>{self.title}</i>'

        # ed = f', {self.edition}' if self.edition else ''
        vols = f', {self.volumes}' if self.volumes else ''
        # annotation = f' [{self.annotation}]' if self.annotation else ''

        if self.published_locations.all().count() == 1:
            locations = f', {self.published_locations.first()}'
        elif self.published_locations.all().count() > 1:
            locations = f', {"-".join(str(l) for l in self.published_locations.all())}'
        else:
            locations = ''

        if self.published_year and self.published_locations.all().count() > 0:
            year = f' {self.published_year}'
        elif self.published_year and self.published_locations.all().count() == 0:
            year = f', {self.published_year}'
        elif not self.published_year and self.published_locations.all().count() > 0:
            year = ' [b.r.]'
        else:
            # i.e.: not self.published_year and self.published_locations.all().count() == 0:
            year = ', [b.m.], [b.r.]'

        description = f'{authors}{title}' \
            f'{editors_abbrev}{editors}{translators_abbrev}{translators}' \
            f'{vols}{locations}{year}.'

        return format_html(f'{description}')

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)
        self.description = self.__str__()
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        super(Book, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '1. Wydawnictwo zwarte'
        verbose_name_plural = '1. Wydawnictwa zwarte'
        ordering = ['sorting_name']


class Chapter(models.Model):
    authors = models.ManyToManyField(Author, related_name='chapters_as_author', verbose_name='Autorstwo', blank=True)
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)
    # editors_abbrev = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
    #                                   blank=True, null=True)
    # editors = models.ManyToManyField(Author,
    #                                  related_name='chapters_as_editor',
    #                                  verbose_name='Redakcja/Opracowanie itp.',
    #                                  blank=True)
    # translators_abbrev = models.CharField(max_length=100, verbose_name='Skrót tłumaczenia (np. tłum.)',
    #                                       blank=True, null=True)
    # translators = models.ManyToManyField(Translator,
    #                                      related_name='chapters_as_translator',
    #                                      verbose_name='Tłumaczenie',
    #                                      blank=True)

    encompassing_bibliographic_unit = models.ForeignKey(EncompassingBibliographicUnit,
                                                        related_name='dependent_bibliographic_units',
                                                        verbose_name='Opublikowane w: (wydawnictwo zwarte)',
                                                        on_delete=models.PROTECT)
    in_volume = models.CharField(max_length=100, verbose_name='Tom (np. "t. 2")', blank=True, null=True)
    encompassing_bibliographic_unit_pages = models.CharField(max_length=100, verbose_name='Strony (np. "s. 7-77")',
                                                             blank=True, null=True)

    cat_lvl_3 = models.ManyToManyField(CategoryLevelThree,
                                       related_name='chapters',
                                       verbose_name='Kategorie i podkategorie')
    annotation = models.CharField(max_length=10000, verbose_name='Uwagi', blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, related_name='chapters', verbose_name='Wyrażenia kluczowe', blank=True)

    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)
    description = models.CharField(max_length=1000, verbose_name='Opis bibliograficzny (pole automatyczne)',
                                   blank=True, null=True)
    # following field is needed to simplify bibliography_search_view():
    published_year = models.CharField(max_length=100,
                                      verbose_name="Rok wydania wydawnictwa nadrzędnego (pole automatyczne)",
                                      blank=True, null=True)

    def __str__(self):
        # PART 1: elements considering bibliographic unit being part of a book:
        authors = ', '.join(f'{a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
        # editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        # translators = ', '.join(f' {a.first_names} {a.last_name}' for a in self.translators.all()) if self.translators.all() else ''
        # editors_abbrev = f', {self.editors_abbrev}' if self.editors_abbrev else ''
        # translators_abbrev = f', {self.translators_abbrev}' if self.translators_abbrev else ''

        if self.title and self.authors.all().count() > 0:
            title = f', <i>{self.title}</i>'
        elif not self.title:
            title = ', '
        else:
            title = f'<i>{self.title}</i>'

        vol = f', {self.in_volume}' if self.in_volume else ''
        pages = f', {self.encompassing_bibliographic_unit_pages}' if self.encompassing_bibliographic_unit_pages else ''
        # annotation = f' [{self.annotation}]' if self.annotation else ''

        # PART 2: elements considering encompassing bibliographic unit:
        unit = self.encompassing_bibliographic_unit
        u_authors = ', '.join(f' {a.first_names} {a.last_name}' for a in unit.authors.all()) if unit.authors.all() else ''
        u_translators = f' {", ".join(str(t) for t in unit.translators.all())}' if unit.translators.all() else ''
        u_editors = ', '.join(f' {a.first_names} {a.last_name}' for a in unit.editors.all()) if unit.editors.all() else ''

        u_editors_abbrev = f', {unit.editors_abbrev}' if unit.editors_abbrev else ''
        u_translators_abbrev = f', {unit.translators_abbrev}' if unit.translators_abbrev else ''

        if unit.title and unit.authors.all().count() > 0:
            u_title = f', <i>{unit.title}</i>'
        else:
            u_title = f'<i>{unit.title}</i>'

        # u_ed = f', {unit.edition}' if unit.edition else ''

        if unit.published_locations.all().count() == 1:
            u_locations = f', {unit.published_locations.first()}'
        elif unit.published_locations.all().count() > 1:
            u_locations = f', {"-".join(str(l) for l in unit.published_locations.all())}'
        else:
            u_locations = ''

        if unit.published_year and unit.published_locations.all().count() > 0:
            u_year = f' {unit.published_year}'
        elif unit.published_year and unit.published_locations.all().count() == 0:
            u_year = f', {unit.published_year}'
        elif not unit.published_year and unit.published_locations.all().count() > 0:
            u_year = ' [b.r.]'
        else:
            # i.e.: not unit.published_year and unit.published_locations.all().count() == 0:
            u_year = ', [b.m.], [b.r.]'

        unit = f', [w:] {u_authors}{u_title}' \
            f'{vol}{u_editors_abbrev}{u_editors}{u_translators_abbrev}{u_translators}' \
            f'{u_locations}{u_year}'

        description = f'{authors}{title}{unit}{pages}.'
        # f'{editors_abbrev}{editors}' \
        # f'{translators_abbrev}{translators}' \

        return format_html(f'{description}')

    def save(self, *args, **kwargs):
        super(Chapter, self).save(*args, **kwargs)
        self.description = self.__str__()
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        self.published_year = self.encompassing_bibliographic_unit.published_year
        super(Chapter, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '2. Rozdział/artykuł/hasło w wydawnictwie zwartym'
        verbose_name_plural = '2. Rozdziały/artykuły/hasła w wydawnictwach zwartych'
        ordering = ['sorting_name']


class Article(models.Model):
    authors = models.ManyToManyField(Author, related_name='articles_as_author', verbose_name='Autorstwo', blank=True)
    title = models.CharField(max_length=1000, verbose_name='Tytuł', blank=True, null=True)
    # editors_abbrev = models.CharField(max_length=100, verbose_name='Skrót redakcji/opracowania itp. (np. red.)',
    #                                   blank=True, null=True)
    # editors = models.ManyToManyField(Author,
    #                                  related_name='articles_as_editor',
    #                                  verbose_name='Redakcja/Opracowanie itp.',
    #                                  blank=True)
    # translators_abbrev = models.CharField(max_length=100, verbose_name='Skrót tłumaczenia (np. tłum.)',
    #                                       blank=True, null=True)
    # translators = models.ManyToManyField(Translator,
    #                                      related_name='articles_as_translator',
    #                                      verbose_name='Tłumaczenie',
    #                                      blank=True)

    periodical = models.ForeignKey(Periodical,
                                   related_name='contained_articles',
                                   verbose_name='Opublikowane w: (periodyk)',
                                   on_delete=models.PROTECT)
    periodical_pages = models.CharField(max_length=100, verbose_name='Strony (np. "str. 7-77")', blank=True, null=True)

    cat_lvl_3 = models.ManyToManyField(CategoryLevelThree,
                                       related_name='articles',
                                       verbose_name='Kategorie i podkategorie')
    annotation = models.CharField(max_length=10000, verbose_name='Uwagi', blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, related_name='articles', verbose_name='Wyrażenia kluczowe', blank=True)

    sorting_name = models.CharField(max_length=1000, verbose_name='Nazwa sortująca (wypełniana automatycznie)',
                                    blank=True, null=True)
    description = models.CharField(max_length=1000, verbose_name='Opis bibliograficzny (pole automatyczne)',
                                   blank=True, null=True)
    # following field is needed to simplify bibliography_search_view():
    published_year = models.CharField(max_length=100,
                                      verbose_name="Rok wydania periodyku (pole automatyczne)",
                                      blank=True, null=True)

    def __str__(self):
        authors = ', '.join(f' {a.last_name} {a.first_names}' for a in self.authors.all()) if self.authors.all() else ''
        # editors = ', '.join(f' {a.first_names} {a.last_name}' for a in self.editors.all()) if self.editors.all() else ''
        # translators = ', '.join(f' {a.first_names} {a.last_name}' for a in self.translators.all()) if self.translators.all() else ''
        # editors_abbrev = f', {self.editors_abbrev}' if self.editors_abbrev else ''
        # translators_abbrev = f', {self.translators_abbrev}' if self.translators_abbrev else ''

        if self.title and self.authors.all().count() > 0:
            title = f', <i>{self.title}</i>'
        elif not self.title:
            title = ', '
        else:
            title = f'<i>{self.title}</i>'

        pages = f', {self.periodical_pages}' if self.periodical_pages else ''
        # annotation = f' [{self.annotation}]' if self.annotation else ''
        periodical = f', {self.periodical}'

        description = f'{authors}{title}{periodical}{pages}.'
        # f'{editors_abbrev}{editors}' \
        # f'{translators_abbrev}{translators}' \

        return format_html(f'{description}')

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        self.description = self.__str__()
        self.sorting_name = replace_special_chars(remove_tags(self.__str__()))
        self.published_year = self.periodical.published_year
        super(Article, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '3. Artykuł w periodyku'
        verbose_name_plural = '3. Artykuły w periodykach'
        ordering = ['sorting_name']


def save_again(sender, instance, **kwargs):
    """Saves sender instance again to populate fields based on m2m fields of the same model"""
    instance.save()


m2m_changed.connect(save_again, sender=Book.authors.through)
m2m_changed.connect(save_again, sender=Book.editors.through)
m2m_changed.connect(save_again, sender=Book.translators.through)
m2m_changed.connect(save_again, sender=Book.published_locations.through)
m2m_changed.connect(save_again, sender=Chapter.authors.through)
m2m_changed.connect(save_again, sender=Article.authors.through)
