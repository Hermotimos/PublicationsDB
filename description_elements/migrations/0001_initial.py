# Generated by Django 2.2 on 2019-11-26 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_names', models.CharField(blank=True, max_length=100, null=True, verbose_name='Imię/Imiona')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nazwisko')),
                ('sorting_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nazwa sortująca (pole automatyczne)')),
            ],
            options={
                'verbose_name': '1. Autor/Redaktor',
                'verbose_name_plural': '1. Autorzy i redaktorzy',
                'ordering': ['sorting_name'],
                'unique_together': {('first_names', 'last_name')},
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Wyrażenie kluczowe')),
                ('sorting_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nazwa sortująca (pole automatyczne)')),
            ],
            options={
                'verbose_name': '4. Wyrażenie kluczowe',
                'verbose_name_plural': '4. Wyrażenia kluczowe',
                'ordering': ['sorting_name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Miejscowość')),
                ('sorting_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nazwa sortująca (pole automatyczne)')),
            ],
            options={
                'verbose_name': '3. Miejscowość',
                'verbose_name_plural': '3. Miejscowości',
                'ordering': ['sorting_name'],
            },
        ),
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_names', models.CharField(blank=True, max_length=100, null=True, verbose_name='Imię/Imiona')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nazwisko')),
                ('sorting_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nazwa sortująca (pole automatyczne)')),
            ],
            options={
                'verbose_name': '2. Tłumacz',
                'verbose_name_plural': '2. Tłumacze',
                'ordering': ['sorting_name'],
                'unique_together': {('first_names', 'last_name')},
            },
        ),
        migrations.CreateModel(
            name='Periodical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='Tytuł periodyku')),
                ('published_year', models.CharField(blank=True, max_length=20, null=True, verbose_name='Rok wydania')),
                ('vol_info_lvl_1', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numeracja wolumenu poziom 1')),
                ('vol_info_lvl_2', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numeracja wolumenu poziom 2')),
                ('vol_info_lvl_3', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numeracja wolumenu poziom 3')),
                ('sorting_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nazwa sortująca (wypełniana automatycznie)')),
            ],
            options={
                'verbose_name': '5. Periodyk',
                'verbose_name_plural': '5. Periodyki',
                'ordering': ['sorting_name'],
                'unique_together': {('title', 'published_year', 'vol_info_lvl_1', 'vol_info_lvl_2', 'vol_info_lvl_3')},
            },
        ),
        migrations.CreateModel(
            name='EncompassingBibliographicUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='Tytuł')),
                ('translators_abbrev', models.CharField(blank=True, max_length=100, null=True, verbose_name='Skrót tłumaczenia (np. tłum.)')),
                ('sorting_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nazwa sortująca (wypełniana automatycznie)')),
                ('authors', models.ManyToManyField(blank=True, related_name='encompassing_bib_units_as_author', to='description_elements.Author', verbose_name='Autorstwo')),
                ('translators', models.ManyToManyField(blank=True, related_name='encompassing_bib_units_as_translator', to='description_elements.Translator', verbose_name='Tłumaczenie')),
            ],
            options={
                'verbose_name': '6. Wydawnictwo zwarte nadrzędne',
                'verbose_name_plural': '6. Wydawnictwa zwarte nadrzędne',
                'ordering': ['sorting_name'],
            },
        ),
    ]