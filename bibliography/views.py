from django.shortcuts import render, redirect
from django.db.models import Q

from bibliography.models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical
from categories.models import CategoryLevelOne
from publications_db.utils import replace_special_chars


def bibliography_main_view(request):
    books = [obj for obj in BibliographicUnitBook.objects.all()]
    parts_of_books = [obj for obj in BibliographicUnitPartOfBook.objects.all()]
    parts_of_periodicals = [obj for obj in BibliographicUnitPartOfPeriodical.objects.all()]
    all_descriptions = books + parts_of_books + parts_of_periodicals
    sorted_descriptions = sorted(all_descriptions, key=lambda desc: replace_special_chars(desc.description))

    context = {
        'page_title': 'Strona główna',
        'descriptions': sorted_descriptions,
    }
    return render(request, 'bibliography/bibliography_main.html', context)


def bibliography_full_view(request):
    books = [obj for obj in BibliographicUnitBook.objects.all()]
    parts_of_books = [obj for obj in BibliographicUnitPartOfBook.objects.all()]
    parts_of_periodicals = [obj for obj in BibliographicUnitPartOfPeriodical.objects.all()]
    all_descriptions = books + parts_of_books + parts_of_periodicals
    sorted_descriptions = sorted(all_descriptions, key=lambda desc: replace_special_chars(desc.description))

    context = {
        'page_title': 'Pełna bibliografia',
        'descriptions': sorted_descriptions,
    }
    return render(request, 'bibliography/bibliography_full.html', context)


def bibliography_index_view(request):
    books = [obj for obj in BibliographicUnitBook.objects.all()]
    parts_of_books = [obj for obj in BibliographicUnitPartOfBook.objects.all()]
    parts_of_periodicals = [obj for obj in BibliographicUnitPartOfPeriodical.objects.all()]
    all_descriptions = books + parts_of_books + parts_of_periodicals

    # Version 1: shows all categories and subcategories regardless whether they contain any descriptions or not
    # cat1_with_cat2_with_cat3_dict = {
    #     cat1: {
    #         cat2: [
    #             cat3 for cat3 in cat2.categories_lvl_3.all()
    #         ] for cat2 in cat1.categories_lvl_2.all()
    #     } for cat1 in CategoryLevelOne.objects.all()
    # }

    # Version 2: shows only categories and subcategories containing at least 1 description
    def is_not_empty_cat3(category3):
        """Returns 0 for False if category is empty, else >0 for True if not empty"""
        return category3.bib_units_books.count() \
            + category3.bib_units_parts_of_books.count() \
            + category3.bib_units_parts_of_periodicals.count()

    def is_not_empty_cat2(category2):
        for cat3 in category2.categories_lvl_3.all():
            if is_not_empty_cat3(cat3):
                return True
        return False

    def is_not_empty_cat1(category1):
        for cat2 in category1.categories_lvl_2.all():
            if is_not_empty_cat2(cat2):
                return True
        return False

    cat1_with_cat2_with_cat3_dict = {
        cat1: {
            cat2: [
                cat3 for cat3 in cat2.categories_lvl_3.all() if is_not_empty_cat3(cat3)
            ] for cat2 in cat1.categories_lvl_2.all() if is_not_empty_cat2(cat2)
        } for cat1 in CategoryLevelOne.objects.all() if is_not_empty_cat1(cat1)
    }

    context = {
        'page_title': 'Indeks tematyczny',
        'descriptions': all_descriptions,
        'cat1_with_cat2_with_cat3_dict': cat1_with_cat2_with_cat3_dict,
    }
    return render(request, 'bibliography/bibliography_index.html', context)


def bibliography_search_view(request):
    books_1 = books_2 = BibliographicUnitBook.objects.all()
    parts_of_books_1 = parts_of_books_2 = BibliographicUnitPartOfBook.objects.all()
    parts_of_periodicals_1 = parts_of_periodicals_2 = BibliographicUnitPartOfPeriodical.objects.all()

    query1 = request.GET.get('search1')
    query2 = request.GET.get('search2')
    option1 = request.GET.get('option1')
    option2 = request.GET.get('option2')
    operator = request.GET.get('operator')
    is_searching = False

    # TODO add 'editors' field to filters (if client wants it) - together or separate from author?

    if query1:
        is_searching = True
        if option1 == 'all':
            books_1 = books_1.filter(description__icontains=query1)
            parts_of_books_1 = parts_of_books_1.filter(description__icontains=query1)
            parts_of_periodicals_1 = parts_of_periodicals_1.filter(description__icontains=query1)
        elif option1 == 'author':
            books_1 = books_1.filter(authors__last_name__icontains=query1)
            parts_of_books_1 = parts_of_books_1.filter(authors__last_name__icontains=query1)
            parts_of_periodicals_1 = parts_of_periodicals_1.filter(authors__last_name__icontains=query1)
        elif option1 == 'title':
            books_1 = books_1.filter(title__icontains=query1)
            parts_of_books_1 = parts_of_books_1.filter(title__icontains=query1)
            parts_of_periodicals_1 = parts_of_periodicals_1.filter(title__icontains=query1)
        elif option1 == 'year':
            books_1 = books_1.filter(published_year__icontains=query1)
            parts_of_books_1 = parts_of_books_1.filter(published_year__icontains=query1)
            parts_of_periodicals_1 = parts_of_periodicals_1.filter(published_year__icontains=query1)

            descriptions_2 = []

    if query1 and query2 and operator == 'and':
        if option2 == 'all':
            books_2 = books_2.filter(description__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(description__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(description__icontains=query2)
        elif option2 == 'author':
            books_2 = books_2.filter(authors__last_name__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(authors__last_name__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(authors__last_name__icontains=query2)
        elif option2 == 'title':
            books_2 = books_2.filter(title__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(title__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(title__icontains=query2)
        elif option2 == 'year':
            books_2 = books_2.filter(published_year__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(published_year__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(published_year__icontains=query2)

            books_2 = [obj for obj in books_2]
            parts_of_books_2 = [obj for obj in parts_of_books_2]
            parts_of_periodicals_2 = [obj for obj in parts_of_periodicals_2]
            descriptions_2 = books_2 + parts_of_books_2 + parts_of_periodicals_2


    elif query1 and query2 and operator == 'or':
        if option2 == 'all':
            books_2 = books_2.filter(description__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(description__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(description__icontains=query2)
        elif option2 == 'author':
            books_2 = books_2.filter(authors__last_name__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(authors__last_name__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(authors__last_name__icontains=query2)
        elif option2 == 'title':
            books_2 = books_2.filter(title__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(title__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(title__icontains=query2)
        elif option2 == 'year':
            books_2 = books_2.filter(published_year__icontains=query2)
            parts_of_books_2 = parts_of_books_2.filter(published_year__icontains=query2)
            parts_of_periodicals_2 = parts_of_periodicals_2.filter(published_year__icontains=query2)

            books_2 = [obj for obj in books_2]
            parts_of_books_2 = [obj for obj in parts_of_books_2]
            parts_of_periodicals_2 = [obj for obj in parts_of_periodicals_2]
            descriptions_2 = books_2 + parts_of_books_2 + parts_of_periodicals_2

    books_1 = [obj for obj in books_1]
    parts_of_books_1 = [obj for obj in parts_of_books_1]
    parts_of_periodicals_1 = [obj for obj in parts_of_periodicals_1]
    descriptions_1 = books_1 + parts_of_books_1 + parts_of_periodicals_1

    if operator == 'none':
        descriptions = descriptions_1
    elif operator == 'and':
        descriptions = descriptions_2 # TODO this is wrong, just put it here to make view work
    elif operator == 'or':
        descriptions = descriptions_1 + descriptions_2

    sorted_results = sorted(descriptions, key=lambda desc: replace_special_chars(desc.description))

    context = {
        'page_title': 'Wyszukiwanie',
        'sorted_results': sorted_results,
        'is_searching': is_searching
    }
    return render(request, 'bibliography/bibliography_search.html', context)


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
