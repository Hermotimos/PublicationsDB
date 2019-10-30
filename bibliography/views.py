from django.shortcuts import render, redirect
from bibliography.models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical
from categories.models import CategoryLevelOne, CategoryLevelTwo, CategoryLevelThree
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

    cat1_with_cat2_with_cat3_dict = {
        cat1: {
            cat2: [
                cat3 for cat3 in cat2.categories_lvl_3.all()
            ] for cat2 in cat1.categories_lvl_2.all()
        } for cat1 in CategoryLevelOne.objects.all()
    }

    context = {
        'page_title': 'Indeks tematyczny',
        'descriptions': all_descriptions,
        'cat1_with_cat2_with_cat3_dict': cat1_with_cat2_with_cat3_dict,
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
