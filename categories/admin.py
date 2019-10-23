from django.contrib import admin
from .models import Category, SubcategoryLevelOne, SubcategoryLevelTwo, SubcategoryLevelThree, SubcategoryLevelFour

admin.site.register(Category)
admin.site.register(SubcategoryLevelOne)
admin.site.register(SubcategoryLevelTwo)
admin.site.register(SubcategoryLevelThree)
admin.site.register(SubcategoryLevelFour)
