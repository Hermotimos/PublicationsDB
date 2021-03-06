from django.db import models
from django.db.models.signals import post_save

from description_elements.models import Keyword
from publications_db.utils import replace_special_chars, remove_tags


class CategoryLevelOne(models.Model):
    name = models.CharField(max_length=50, verbose_name='Kategoria poz. 1 (max. 50 znaków)', unique=True)
    sorting_name = models.CharField(max_length=200, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)

    class Meta:
        verbose_name = 'Kategoria poz. 1'
        verbose_name_plural = 'Kategorie poz. 1'
        ordering = ['sorting_name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(CategoryLevelOne, self).save(*args, **kwargs)
        self.sorting_name = replace_special_chars(remove_tags(self.name))
        super(CategoryLevelOne, self).save(*args, **kwargs)
        subcategories = self.categories2.all()

        if subcategories.count() == 0:
            self.categories2.create()
        elif subcategories.count() > 0 and any(cat.name != '---' for cat in subcategories.all()):
            for cat in subcategories.all():
                if cat.name == '---':
                    cat.delete()


class CategoryLevelTwo(models.Model):
    cat_lvl_1 = models.ForeignKey(CategoryLevelOne,
                                  related_name='categories2',
                                  on_delete=models.CASCADE,
                                  verbose_name='Kategoria poz. 1')
    name = models.CharField(max_length=100, default='---', verbose_name='Kategoria poz. 2 (max. 100 znaków)')
    formatted_name = models.CharField(max_length=255, default='---', verbose_name='Kategoria poz. 2 pełna nazwa')
    sorting_name = models.CharField(max_length=200, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)

    class Meta:
        verbose_name = 'Kategoria poz. 2'
        verbose_name_plural = 'Kategorie poz. 2'
        ordering = ['cat_lvl_1', 'sorting_name']
        unique_together = ['cat_lvl_1', 'name']

    def __str__(self):
        return f'{self.cat_lvl_1} / {self.name}'

    def save(self, *args, **kwargs):
        # super(CategoryLevelTwo, self).save(*args, **kwargs)
        formatted_name = self.__str__()
        self.formatted_name = formatted_name.replace(' / ---', '')
        self.sorting_name = replace_special_chars(remove_tags(self.name))
        super(CategoryLevelTwo, self).save(*args, **kwargs)

        subcategories = self.categories3
        sister_categories = self.cat_lvl_1.categories2.all()

        if subcategories.count() == 0:
            self.categories3.create()
        elif subcategories.count() > 0 and any(cat.name != '---' for cat in subcategories.all()):
            for cat in subcategories.all():
                if cat.name == '---':
                    cat.delete()

        if sister_categories.count() > 1 and any(cat.name != '---' for cat in sister_categories.all()):
            for cat in sister_categories.all():
                if cat.name == '---':
                    cat.delete()


class CategoryLevelThree(models.Model):
    cat_lvl_2 = models.ForeignKey(CategoryLevelTwo,
                                  related_name='categories3',
                                  on_delete=models.CASCADE,
                                  verbose_name='Kategoria poz. 2')
    name = models.CharField(max_length=105, default='---', verbose_name='Kategoria poz. 3 (max. 105 znaków)')
    formatted_name = models.CharField(max_length=255, default='---', verbose_name='Kategoria poz. 3 pełna nazwa')
    sorting_name = models.CharField(max_length=200, verbose_name='Nazwa sortująca (pole automatyczne)',
                                    blank=True, null=True)

    class Meta:
        verbose_name = 'Kategoria poz. 3'
        verbose_name_plural = 'Kategorie poz. 3'
        ordering = ['cat_lvl_2', 'sorting_name']
        unique_together = ['cat_lvl_2', 'name']

    def __str__(self):
        return f'{self.cat_lvl_2} / {self.name}'

    def save(self, *args, **kwargs):
        # super(CategoryLevelThree, self).save(*args, **kwargs)
        formatted_name = self.__str__()
        self.formatted_name = formatted_name.replace(' / ---', '')
        self.sorting_name = replace_special_chars(remove_tags(self.name))
        super(CategoryLevelThree, self).save(*args, **kwargs)

        if self.cat_lvl_2.categories3.count() > 1:
            for cat3 in self.cat_lvl_2.categories3.all():
                if cat3.name == '---':
                    cat3.delete()


def create_keyword(sender, instance, **kwargs):
    if instance.cat_lvl_2.cat_lvl_1.name == 'Ludzie KUL':
        keywords = [k.name for k in Keyword.objects.all()]
        if instance.name not in keywords:
            new_keyword = Keyword(name=instance.name)
            new_keyword.save()


post_save.connect(create_keyword, sender=CategoryLevelThree)
