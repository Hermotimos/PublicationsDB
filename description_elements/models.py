from django.db import models


class Author(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Inicjał/y')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'

    def __str__(self):
        return f'{self.last_name}, {self.first_names}'


class Translator(models.Model):
    first_names = models.CharField(max_length=100, verbose_name='Inicjał/y')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Tłumacz'
        verbose_name_plural = 'Tłumacze'

    def __str__(self):
        return f'{self.last_name}, {self.first_names}'


class Location(models.Model):
    name = models.CharField(max_length=500, verbose_name="Miejscowość")

    class Meta:
        verbose_name = 'Miejscowość'
        verbose_name_plural = 'Miejscowości'

    def __str__(self):
        return self.name
