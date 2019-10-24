from categories.apps import CategoriesConfig
from bibliography.apps import BibliographyConfig
from description_elements.apps import DescriptionElementsConfig


class KategorieConfig(CategoriesConfig):
    verbose_name = 'III. Kategorie'


class BibliografiaConfig(BibliographyConfig):
    verbose_name = 'I. Opisy bibliograficzne'


class ElementyOpisuBibliograficznegoConfig(DescriptionElementsConfig):
    verbose_name = 'II. Elementy składowe opisu bibliograficznego'
