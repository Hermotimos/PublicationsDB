from django.db import models


class CategoryLevelOne(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Kategoria poz. 1')

    class Meta:
        verbose_name = 'Kategoria poz. 1'
        verbose_name_plural = 'Kategorie poz. 1'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(CategoryLevelOne, self).save(*args, **kwargs)
        if self.categories2.count() == 0:
            self.categories2.create()

        elif self.categories2.count() > 0:
            for cat2 in CategoryLevelTwo.objects.filter(cat_lvl_1=self):
                if cat2.name == '---':
                    cat2.delete()


class CategoryLevelTwo(models.Model):
    cat_lvl_1 = models.ForeignKey(CategoryLevelOne,
                                  related_name='categories2',
                                  on_delete=models.CASCADE,
                                  verbose_name='Kategoria poz. 1')
    name = models.CharField(max_length=1000, default='---', verbose_name='Kategoria poz. 2')
    formatted_name = models.CharField(max_length=1000, default='---', verbose_name='Kategoria poz. 2 pełna nazwa')

    class Meta:
        verbose_name = 'Kategoria poz. 2'
        verbose_name_plural = 'Kategorie poz. 2'
        ordering = ['cat_lvl_1', 'name']

    def __str__(self):
        return f'{self.cat_lvl_1} / {self.name}'

    def save(self, *args, **kwargs):
        # super(CategoryLevelTwo, self).save(*args, **kwargs)
        full_name = self.__str__()
        self.formatted_name = full_name.replace(' / ---', '')
        super(CategoryLevelTwo, self).save(*args, **kwargs)

        if self.categories3.count() == 0:
            self.categories3.create()

        elif self.categories3.count() > 0:
            for cat3 in CategoryLevelThree.objects.filter(cat_lvl_2=self):
                if cat3.name == '---':
                    cat3.delete()

        if self.cat_lvl_1.categories2.count() > 1:
            for cat2 in self.cat_lvl_1.categories2.all():
                if cat2.name == '---':
                    cat2.delete()


class CategoryLevelThree(models.Model):
    cat_lvl_2 = models.ForeignKey(CategoryLevelTwo,
                                  related_name='categories3',
                                  on_delete=models.CASCADE,
                                  verbose_name='Kategoria poz. 2')
    name = models.CharField(max_length=1000, default='---', verbose_name='Kategoria poz. 3')
    formatted_name = models.CharField(max_length=1000, default='---', verbose_name='Kategoria poz. 3 pełna nazwa')

    class Meta:
        verbose_name = 'Kategoria poz. 3'
        verbose_name_plural = 'Kategorie poz. 3'
        ordering = ['cat_lvl_2', 'name']

    def __str__(self):
        return f'{self.cat_lvl_2} / {self.name}'

    def save(self, *args, **kwargs):
        # super(CategoryLevelThree, self).save(*args, **kwargs)
        full_name = self.__str__()
        self.formatted_name = full_name.replace(' / ---', '')
        super(CategoryLevelThree, self).save(*args, **kwargs)

        if self.cat_lvl_2.categories3.count() > 1:
            for cat3 in self.cat_lvl_2.categories3.all():
                if cat3.name == '---':
                    cat3.delete()
