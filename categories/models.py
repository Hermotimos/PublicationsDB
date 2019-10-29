from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Kategoria')

    class Meta:
        verbose_name = 'Kategoria poz. 1'
        verbose_name_plural = 'Kategorie poz. 1'
        ordering = ['name']

    def __str__(self):
        return self.name


class SubcategoryLevelOne(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='subcategories_lvl_1',
                                 on_delete=models.CASCADE,
                                 verbose_name='Kategoria')
    name = models.CharField(max_length=1000, default='n/a', verbose_name='Podkategoria poz. 1')

    class Meta:
        verbose_name = 'Kategoria poz. 2'
        verbose_name_plural = 'Kategorie poz. 2'
        ordering = ['category', 'name']

    def __str__(self):
        if self.name != 'n/a':
            return f'{self.category} / {self.name}'
        else:
            return f'{self.category} / ---'


class SubcategoryLevelTwo(models.Model):
    subcategory_lvl_1 = models.ForeignKey(SubcategoryLevelOne,
                                          related_name='subcategories_lvl_2',
                                          on_delete=models.CASCADE,
                                          verbose_name='Podkategoria poz. 1')
    name = models.CharField(max_length=1000, default='n/a', verbose_name='Podkategoria poz. 2')

    class Meta:
        verbose_name = 'Kategoria poz. 3'
        verbose_name_plural = 'Kategorie poz. 3'
        ordering = ['subcategory_lvl_1', 'name']

    def __str__(self):
        if self.name != 'n/a':
            return f'{self.subcategory_lvl_1} / {self.name}'
        else:
            return f'{self.subcategory_lvl_1} / ---'


# class SubcategoryLevelThree(models.Model):
#     subcategory_lvl_2 = models.ForeignKey(SubcategoryLevelTwo,
#                                           related_name='subcategories_lvl_3',
#                                           on_delete=models.CASCADE,
#                                           verbose_name='Podkategoria poz. 2')
#     name = models.CharField(max_length=1000, default='n/a', verbose_name='Podkategoria poz. 3')
#
#     class Meta:
#         verbose_name = 'Kategoria poz. 4'
#         verbose_name_plural = 'Kategorie poz. 4'
#         ordering = ['subcategory_lvl_2', 'name']
#
#     def __str__(self):
#         if self.name != 'n/a':
#             return f'{self.subcategory_lvl_2} / {self.name}'
#         else:
#             return f'{self.subcategory_lvl_2} / ---'
#
#
# class SubcategoryLevelFour(models.Model):
#     subcategory_lvl_3 = models.ForeignKey(SubcategoryLevelThree,
#                                           related_name='subcategories_lvl_4',
#                                           on_delete=models.CASCADE,
#                                           verbose_name='Podkategoria poz. 3')
#     name = models.CharField(max_length=1000, default='n/a', verbose_name='Podkategoria poz. 4')
#
#     class Meta:
#         verbose_name = 'Kategoria poz. 5'
#         verbose_name_plural = 'Kategorie poz. 5'
#         ordering = ['subcategory_lvl_3', 'name']
#
#     def __str__(self):
#         if self.name != 'n/a':
#             return f'{self.subcategory_lvl_3} / {self.name}'
#         else:
#             return f'{self.subcategory_lvl_3} / ---'
