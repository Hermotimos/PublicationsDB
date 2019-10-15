from django.db import models


# TODO move Author and Location to another app in order to create division in admin !!!!

class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Miejscowość")
    # TODO add [bmw] for 'brak miejsca wydania' for basic locations

    class Meta:
        verbose_name = 'Miejscowość'
        verbose_name_plural = 'Miejscowości'


class BibliographicUnit(models.Model):
    authorship_type = models.CharField(max_length=30, default='', verbose_name='Rodzaj autorstwa')
    authors = models.ManyToManyField(Author, related_name='bibliographic_units', verbose_name='Autor/Autorzy')
    title = models.CharField(max_length=1000, verbose_name="Tytuł")

    # case A: independent bibliographic unit:
    published_location = models.ManyToManyField(Location, related_name='bibliographic_units', verbose_name='Miejsce/miejsca wydania')
    published_year = models.PositiveSmallIntegerField(verbose_name="Rok wydania")     # TODO add validators: min=1918, max=2099
    volumes = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tomy")
    edition = models.CharField(max_length=100, blank=True, null=True, verbose_name="Wydanie")
    # TODO: ask what else can possible get here

    # case B: published within an independent bibliograhic unit:
    # TODO published_in = models.ManyToManyField(BibliographicUnit, related_name='dependent_bibliographic_units', blank=True, null=True, verbose_name='Opublikowane w:')
    # TODO this should relate to itself: https://stackoverflow.com/questions/11721157/django-many-to-many-m2m-relation-to-same-model
    # PROBABLY THIS WILL DO: published_in = models.ManyToManyField('self', related_name='dependent_bibliographic_units', blank=True, null=True, verbose_name='Opublikowane w:')

    # case C: published within a periodical bibliographic unit:
    periodical_pub_title = models.CharField(max_length=1000, verbose_name="Tytuł periodyku")
    periodical_pub_year = models.PositiveSmallIntegerField(verbose_name="Rok wydania")     # TODO add validators: min=1918, max=2099
    periodical_pub_vol_lvl_1 = models.CharField(max_length=10, verbose_name="Numeracja wolumenu poziom 1")  # TODO make verbose_names more precise - consult client
    periodical_pub_vol_lvl_2 = models.CharField(max_length=10, verbose_name="Numeracja wolumenu poziom 2")  # TODO make verbose_names more precise - consult client
    periodical_pub_vol_lvl_3 = models.CharField(max_length=10, verbose_name="Numeracja wolumenu poziom 3")  # TODO make verbose_names more precise - consult client
    periodical_pub_pages = models.CharField(max_length=20, verbose_name="Strony")

    class Meta:
        verbose_name = 'Opis bibliograficzny'
        verbose_name_plural = 'Opisy bibliograficzne'
