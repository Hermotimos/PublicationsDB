# Generated by Django 2.2 on 2019-12-14 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20191214_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorylevelone',
            options={'ordering': ['sorting_name'], 'verbose_name': 'Kategoria poz. 1', 'verbose_name_plural': 'Kategorie poz. 1'},
        ),
        migrations.AlterModelOptions(
            name='categorylevelthree',
            options={'ordering': ['cat_lvl_2', 'sorting_name'], 'verbose_name': 'Kategoria poz. 3', 'verbose_name_plural': 'Kategorie poz. 3'},
        ),
        migrations.AlterModelOptions(
            name='categoryleveltwo',
            options={'ordering': ['cat_lvl_1', 'sorting_name'], 'verbose_name': 'Kategoria poz. 2', 'verbose_name_plural': 'Kategorie poz. 2'},
        ),
    ]
