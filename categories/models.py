from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.PROTECT)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.category}/{self.name}'
