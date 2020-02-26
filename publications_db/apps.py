from activity_log.apps import ActivityLogConfig
from categories.apps import CategoriesConfig
from bibliography.apps import BibliographyConfig
from description_elements.apps import DescriptionElementsConfig


class DziennikAktywnosciConfig(ActivityLogConfig):
    verbose_name = 'Dziennik aktywności'


class KategorieConfig(CategoriesConfig):
    verbose_name = 'III. Kategorie'


class BibliografiaConfig(BibliographyConfig):
    verbose_name = 'I. Opisy bibliograficzne'


class ElementyOpisuBibliograficznegoConfig(DescriptionElementsConfig):
    verbose_name = 'II. Elementy składowe opisu bibliograficznego'
