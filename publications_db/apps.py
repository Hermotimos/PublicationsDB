from categories.apps import CategoriesConfig
from bibliography.apps import BibliographyConfig
from description_elements.apps import DescriptionElementsConfig


class KategorieConfig(CategoriesConfig):
    verbose_name = 'Kategorie'


class BibliografiaConfig(BibliographyConfig):
    verbose_name = 'Bibliografia'


class ElementyOpisuBibliograficznegoConfig(DescriptionElementsConfig):
    verbose_name = 'Elementy opisu bibliograficznego'
