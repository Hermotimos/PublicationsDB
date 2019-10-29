from django.shortcuts import render, redirect
from bibliography.models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical
from publications_db.utils import replace_special_chars


def bibliography_full_view(request):
    books = [obj.description for obj in BibliographicUnitBook.objects.all()]
    parts_of_books = [obj.description for obj in BibliographicUnitPartOfBook.objects.all()]
    parts_of_periodicals = [obj.description for obj in BibliographicUnitPartOfPeriodical.objects.all()]
    all_descriptions = books + parts_of_books + parts_of_periodicals
    sorted_descriptions = sorted(all_descriptions, key=lambda desc: replace_special_chars(desc))

    context = {
        'page_title': 'Pełna bibliografia',
        'descriptions': sorted_descriptions,
    }
    return render(request, 'bibliography/bibliography_full.html', context)


def bibliography_main_view(request):
    books = [obj.description for obj in BibliographicUnitBook.objects.all()]
    parts_of_books = [obj.description for obj in BibliographicUnitPartOfBook.objects.all()]
    parts_of_periodicals = [obj.description for obj in BibliographicUnitPartOfPeriodical.objects.all()]
    all_descriptions = books + parts_of_books + parts_of_periodicals
    sorted_descriptions = sorted(all_descriptions, key=lambda desc: replace_special_chars(desc))

    context = {
        'page_title': 'Strona główna',
        'descriptions': sorted_descriptions,
    }
    return render(request, 'bibliography/bibliography_main.html', context)


def bibliography_index_view(request):
    books = [obj for obj in BibliographicUnitBook.objects.all()]
    parts_of_books = [obj for obj in BibliographicUnitPartOfBook.objects.all()]
    parts_of_periodicals = [obj for obj in BibliographicUnitPartOfPeriodical.objects.all()]
    all_descriptions = books + parts_of_books + parts_of_periodicals

    categories_1 = list(CategoryLevelOne.objects.all())
    categories_2 = list(CategoryLevelTwo.objects.all())
    categories_3 = list(CategoryLevelThree.objects.all())

    cat1_with_descs = [cat for cat in categories_1 if cat.categories_lvl_2.count() == 1]
    cat2_with_descs = {}
    cat3_with_descs = {}

    for desc in all_descriptions:
        if desc.cat_lvl_3 == 'n/a' and desc.cat_lvl_3.cat_lvl_2 == 'n/a':
            if not cat1_with_descs[desc.cat_lvl_3.cat_lvl_2.cat_lvl_1]:
                cat1_with_descs[desc.cat_lvl_3.cat_lvl_2.cat_lvl_1] = (desc, )
            else:
                cat1_with_descs[desc.cat_lvl_3.cat_lvl_2.cat_lvl_1].append(desc)

    context = {
        'page_title': 'Indeks tematyczny',
        'descriptions': all_descriptions,
        'categories': categories_1,
        'subcategories_1': categories_2,
        'subcategories_2': categories_3,
        'cat1_with_descs': cat1_with_descs,
        'cat2_with_descs': cat2_with_descs,
        'cat3_with_descs': cat3_with_descs
    }
    return render(request, 'bibliography/bibliography_index.html', context)


def bibliography_search_view(request):
    pass


def bibliography_search_results_view(request):
    pass


def bibliography_reload_view(request):
    for obj in BibliographicUnitBook.objects.all():
        obj.save()
    for obj in BibliographicUnitPartOfBook.objects.all():
        obj.save()
    for obj in BibliographicUnitPartOfPeriodical.objects.all():
        obj.save()
    return redirect('bibliography:main')
