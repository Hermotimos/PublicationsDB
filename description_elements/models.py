from django.db import models


class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Imię/Imiona', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'
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
