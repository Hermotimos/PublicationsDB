from django.shortcuts import render
from bibliography.models import BibliographicUnitBook, BibliographicUnitPartOfBook, BibliographicUnitPartOfPeriodical
from publications_db.utils import sort_pl


def bibliography_main_view(request):
    books = [obj.description for obj in BibliographicUnitBook.objects.all()]
    parts_of_books = [obj.description for obj in BibliographicUnitPartOfBook.objects.all()]
    parts_of_periodicals = [obj.description for obj in BibliographicUnitPartOfPeriodical.objects.all()]
    all_descriptions = books + parts_of_books + parts_of_periodicals
    sorted_descriptions = sorted(all_descriptions, key=lambda desc: sort_pl(desc))

    context = {
        'page_title': 'Strona główna',
        'descriptions': sorted_descriptions,
    }
    return render(request, 'bibliography/bibliography_main.html', context)
