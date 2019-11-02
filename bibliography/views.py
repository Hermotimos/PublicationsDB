from django.shortcuts import render, redirect
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
    books_qs = BibliographicUnitBook.objects.all()
    parts_of_books_qs = BibliographicUnitPartOfBook.objects.all()
    parts_of_periodicals_qs = BibliographicUnitPartOfPeriodical.objects.all()

    query1 = request.GET.get('search1')
    option1 = request.GET.get('option1')
    query2 = request.GET.get('search2')
    option2 = request.GET.get('option2')
    query3 = request.GET.get('search3')
    option3 = request.GET.get('option3')
    query4 = request.GET.get('search4')
    option4 = request.GET.get('option4')

    # TODO add 'editors' field to filters (if client wants it) - together or separate from author?

    if query1:
        if option1 == 'all':
            books_qs = books_qs.filter(description__icontains=query1)
            parts_of_books_qs = parts_of_books_qs.filter(description__icontains=query1)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(description__icontains=query1)
        elif option1 == 'author':
            books_qs = books_qs.filter(authors__last_name__icontains=query1)
            parts_of_books_qs = parts_of_books_qs.filter(authors__last_name__icontains=query1)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(authors__last_name__icontains=query1)
        elif option1 == 'title':
            books_qs = books_qs.filter(title__icontains=query1)
            parts_of_books_qs = parts_of_books_qs.filter(title__icontains=query1)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(title__icontains=query1)
        elif option1 == 'year':
            books_qs = books_qs.filter(published_year__icontains=query1)
            parts_of_books_qs = parts_of_books_qs.filter(encompassing_bibliographic_unit__published_year__icontains=query1)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(periodical__published_year__icontains=query1)

    if query2:
        if option2 == 'all':
            books_qs = books_qs.filter(description__icontains=query2)
            parts_of_books_qs = parts_of_books_qs.filter(description__icontains=query2)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(description__icontains=query2)
        elif option2 == 'author':
            books_qs = books_qs.filter(authors__last_name__icontains=query2)
            parts_of_books_qs = parts_of_books_qs.filter(authors__last_name__icontains=query2)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(authors__last_name__icontains=query2)
        elif option2 == 'title':
            books_qs = books_qs.filter(title__icontains=query2)
            parts_of_books_qs = parts_of_books_qs.filter(title__icontains=query2)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(title__icontains=query2)
        elif option2 == 'year':
            books_qs = books_qs.filter(published_year__icontains=query2)
            parts_of_books_qs = parts_of_books_qs.filter(encompassing_bibliographic_unit__published_year__icontains=query2)
            parts_of_periodicals_qs = parts_of_periodicals_qs.filter(periodical__published_year__icontains=query2)

    books = [obj for obj in books_qs]
    parts_of_books = [obj for obj in parts_of_books_qs]
    parts_of_periodicals = [obj for obj in parts_of_periodicals_qs]
    descriptions = books + parts_of_books + parts_of_periodicals
    sorted_results = sorted(descriptions, key=lambda desc: replace_special_chars(desc.description))

    context = {
        'page_title': 'Wyszukiwanie',
        'sorted_results': sorted_results,
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
