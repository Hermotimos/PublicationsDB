from django.db import models


# TODO move Author and Location to another app in order to create division in admin !!!!

class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'


class Location(models.Model):
    name = models.CharField(max_length=500, verbose_name="Miejscowość")

    class Meta:
        verbose_name = 'Miejscowość'
        verbose_name_plural = 'Miejscowości'


class BibliographicUnit(models.Model):
    authorship = models.CharField(max_length=100, verbose_name='Rodzaj autorstwa (np. red., oprac.)', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='bibliographic_units', verbose_name='Autor/Autorzy')
    title = models.CharField(max_length=1000, verbose_name="Tytuł", blank=True, null=True)

    # case A: independent bibliographic unit:
    published_location = models.ManyToManyField(Location, related_name='bibliographic_units', verbose_name='Miejsce/miejsca wydania')
    published_year = models.CharField(max_length=100, verbose_name="Rok wydania", blank=True, null=True)
    volumes = models.CharField(max_length=100, verbose_name="Tomy", blank=True, null=True)
    edition = models.CharField(max_length=100, verbose_name="Wydanie", blank=True, null=True)
    # TODO: ask what else can possible get here

    # case B: published within an independent bibliograhic unit:
    # TODO published_in = models.ManyToManyField(BibliographicUnit, related_name='dependent_bibliographic_units', blank=True, null=True, verbose_name='Opublikowane w:')
    # TODO this should relate to itself: https://stackoverflow.com/questions/11721157/django-many-to-many-m2m-relation-to-same-model
    published_in = models.ManyToManyField('self', related_name='dependent_bibliographic_units', verbose_name='Opublikowane w:')

    # case C: published within a periodical bibliographic unit:
    periodical_pub_title = models.CharField(max_length=1000, verbose_name="Tytuł periodyku", blank=True, null=True)
    periodical_pub_year = models.CharField(max_length=100, verbose_name="Rocznik", blank=True, null=True)
    periodical_pub_vol_lvl_1 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 1", blank=True, null=True)  # TODO make verbose_names more precise - consult client
    periodical_pub_vol_lvl_2 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 2", blank=True, null=True)  # TODO make verbose_names more precise - consult client
    periodical_pub_vol_lvl_3 = models.CharField(max_length=100, verbose_name="Numeracja wolumenu poziom 3", blank=True, null=True)  # TODO make verbose_names more precise - consult client
    periodical_pub_pages = models.CharField(max_length=100, verbose_name="Strony", blank=True, null=True)

    class Meta:
        verbose_name = 'Opis bibliograficzny'
        verbose_name_plural = 'Opisy bibliograficzne'
