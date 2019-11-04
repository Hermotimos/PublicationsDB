from django.shortcuts import render, redirect
from django.db.models import Count

from bibliography.models import Book, Chapter, Article
from bibliography.utils import query_debugger
from categories.models import CategoryLevelOne, CategoryLevelTwo, CategoryLevelThree
from publications_db.utils import replace_special_chars


def bibliography_main_view(request):
    books = [obj for obj in Book.objects.all()]
    chapters = [obj for obj in Chapter.objects.all()]
    articles = [obj for obj in Article.objects.all()]
    results = books + chapters + articles

    context = {
        'page_title': 'Strona główna',
        'results': sorted(results, key=lambda desc: replace_special_chars(desc.description)),
    }
    return render(request, 'bibliography/bibliography_main.html', context)


@query_debugger
def bibliography_full_view(request):
    books = [obj for obj in Book.objects.all()]
    chapters = [obj for obj in Chapter.objects.all()]
    articles = [obj for obj in Article.objects.all()]
    results = books + chapters + articles

    context = {
        'page_title': 'Pełna bibliografia',
        'results': sorted(results, key=lambda desc: replace_special_chars(desc.description)),
    }
    return render(request, 'bibliography/bibliography_full.html', context)


@query_debugger
def bibliography_index_view(request):
    # VERSION 1: shows all categories and subcategories regardless whether they contain any descriptions or not
    # Number of Queries : 53
    # Finished in : 0.11s

    cat1_qs = CategoryLevelOne.objects.all().prefetch_related('categories2')
    index = {}
    for cat1 in cat1_qs:
        index[cat1] = {
            cat2: {
                cat3: [
                    unit for unit in
                    list(cat3.books.all())
                    + list(cat3.chapters.all())
                    + list(cat3.articles.all())
                ] for cat3 in cat2.categories3.all().prefetch_related('books', 'chapters', 'articles')
            } for cat2 in cat1.categories2.all()
        }

    # VERSION 2 [VERY COSTLY]: shows only categories and subcategories containing at least 1 description
    # Number of Queries: 376
    # Finished in: 0.36s

    # def is_not_empty_cat3(category3):
    #     """Returns 0 for False if category is empty, else >0 for True if not empty"""
    #     return category3.books.count() \
    #         + category3.chapters.count() \
    #         + category3.articles.count()
    #
    # def is_not_empty_cat2(category2):
    #     for cat3 in category2.categories3.all():
    #         if is_not_empty_cat3(cat3):
    #             return True
    #     return False
    #
    # def is_not_empty_cat1(category1):
    #     for cat2 in category1.categories2.all():
    #         if is_not_empty_cat2(cat2):
    #             return True
    #     return False
    #
    # index = {
    #     cat1: {
    #         cat2: {
    #             cat3: [
    #                 unit for unit in
    #                 list(cat3.books.all())
    #                 + list(cat3.chapters.all())
    #                 + list(cat3.articles.all())
    #             ] for cat3 in cat2.categories3.all() if is_not_empty_cat3(cat3)
    #         } for cat2 in cat1.categories2.all() if is_not_empty_cat2(cat2)
    #     } for cat1 in CategoryLevelOne.objects.all() if is_not_empty_cat1(cat1)
    # }

    context = {
        'page_title': 'Indeks tematyczny',
        'index': index,
    }
    return render(request, 'bibliography/bibliography_index.html', context)


@query_debugger
def bibliography_search_view(request):
    search1 = request.GET.get('search1')
    search2 = request.GET.get('search2')
    option1 = request.GET.get('option1')
    option2 = request.GET.get('option2')
    operator = request.GET.get('operator')
    categories = request.GET.getlist('categories')
    is_categories = request.GET.get('is_categories')

    categories3 = [obj.full_name for obj in CategoryLevelThree.objects.all()]
    # TODO make it a dict and use pk in form and then in filtering

    if is_categories:
        # TODO: following does not work: no results
        books_1 = books_2 = Book.objects.all().filter(cat_lvl_3__full_name__in=categories).prefetch_related('authors')
        chapters_1 = chapters_2 = Chapter.objects.all().filter(cat_lvl_3__name__in=categories).prefetch_related('authors')
        articles_1 = articles_2 = Article.objects.all().filter(cat_lvl_3__name__in=categories).prefetch_related('authors')
    else:
        books_1 = books_2 = Book.objects.all().prefetch_related('authors')
        chapters_1 = chapters_2 = Chapter.objects.all().prefetch_related('authors')
        articles_1 = articles_2 = Article.objects.all().prefetch_related('authors')





    # TODO add 'editors' field to filters (if client wants it) - together or separate from author?

    # CASE 1: search1 is empty (empty form submitted or only search2) => show all objects:
    if not search1:
        is_searching = False
        descriptions = []

    # CASE 2: search1 not empty:
    else:
        is_searching = True

        # Preparation of query1 results:
        if option1 == 'all':
            books_1 = books_1.filter(description__icontains=search1)
            chapters_1 = chapters_1.filter(description__icontains=search1)
            articles_1 = articles_1.filter(description__icontains=search1)
        elif option1 == 'author':
            books_1 = books_1.filter(authors__last_name__icontains=search1)
            chapters_1 = chapters_1.filter(authors__last_name__icontains=search1)
            articles_1 = articles_1.filter(authors__last_name__icontains=search1)
        elif option1 == 'title':
            books_1 = books_1.filter(title__icontains=search1)
            chapters_1 = chapters_1.filter(title__icontains=search1)
            articles_1 = articles_1.filter(title__icontains=search1)
        elif option1 == 'year':
            books_1 = books_1.filter(published_year__icontains=search1)
            chapters_1 = chapters_1.filter(published_year__icontains=search1)
            articles_1 = articles_1.filter(published_year__icontains=search1)

        # CASE 2.1: both queries with 'AND' operator:
        if search1 and search2 and operator == 'and':
            if option2 == 'all':
                books_2 = books_1.filter(description__icontains=search2)
                chapters_2 = chapters_1.filter(description__icontains=search2)
                articles_2 = articles_1.filter(description__icontains=search2)
            elif option2 == 'author':
                books_2 = books_1.filter(authors__last_name__icontains=search2)
                chapters_2 = chapters_1.filter(authors__last_name__icontains=search2)
                articles_2 = articles_1.filter(authors__last_name__icontains=search2)
            elif option2 == 'title':
                books_2 = books_1.filter(title__icontains=search2)
                chapters_2 = chapters_1.filter(title__icontains=search2)
                articles_2 = articles_1.filter(title__icontains=search2)
            elif option2 == 'year':
                books_2 = books_1.filter(published_year__icontains=search2)
                chapters_2 = chapters_1.filter(published_year__icontains=search2)
                articles_2 = articles_1.filter(published_year__icontains=search2)

            books_2 = [obj for obj in books_2]
            chapters_2 = [obj for obj in chapters_2]
            articles_2 = [obj for obj in articles_2]
            descriptions_2 = books_2 + chapters_2 + articles_2

            descriptions = descriptions_2

        # CASE 2.2: both queries with 'OR' operator:
        elif search1 and search2 and operator == 'or':
            if option2 == 'all':
                books_2 = books_2.filter(description__icontains=search2).union(books_1)
                chapters_2 = chapters_2.filter(description__icontains=search2).union(chapters_1)
                articles_2 = articles_2.filter(description__icontains=search2).union(articles_1)
            elif option2 == 'author':
                books_2 = books_2.filter(authors__last_name__icontains=search2).union(books_1)
                chapters_2 = chapters_2.filter(authors__last_name__icontains=search2).union(chapters_1)
                articles_2 = articles_2.filter(authors__last_name__icontains=search2).union(articles_1)
            elif option2 == 'title':
                books_2 = books_2.filter(title__icontains=search2).union(books_1)
                chapters_2 = chapters_2.filter(title__icontains=search2).union(chapters_1)
                articles_2 = articles_2.filter(title__icontains=search2).union(articles_1)
            elif option2 == 'year':
                books_2 = books_2.filter(published_year__icontains=search2).union(books_1)
                chapters_2 = chapters_2.filter(published_year__icontains=search2).union(chapters_1)
                articles_2 = articles_2.filter(published_year__icontains=search2).union(articles_1)

            books_2 = [obj for obj in books_2]
            chapters_2 = [obj for obj in chapters_2]
            articles_2 = [obj for obj in articles_2]
            descriptions_2 = books_2 + chapters_2 + articles_2

            descriptions = descriptions_2

        # CASE 2.3: both queries with 'NOT' operator:
        elif search1 and search2 and operator == 'not':
            if option2 == 'all':
                books_2 = books_1.exclude(description__icontains=search2)
                chapters_2 = chapters_1.exclude(description__icontains=search2)
                articles_2 = articles_1.exclude(description__icontains=search2)
            elif option2 == 'author':
                books_2 = books_1.exclude(authors__last_name__icontains=search2)
                chapters_2 = chapters_1.exclude(authors__last_name__icontains=search2)
                articles_2 = articles_1.exclude(authors__last_name__icontains=search2)
            elif option2 == 'title':
                books_2 = books_1.exclude(title__icontains=search2)
                chapters_2 = chapters_1.exclude(title__icontains=search2)
                articles_2 = articles_1.exclude(title__icontains=search2)
            elif option2 == 'year':
                books_2 = books_1.exclude(published_year__icontains=search2)
                chapters_2 = chapters_1.exclude(published_year__icontains=search2)
                articles_2 = articles_1.exclude(published_year__icontains=search2)

            books_2 = [obj for obj in books_2]
            chapters_2 = [obj for obj in chapters_2]
            articles_2 = [obj for obj in articles_2]
            descriptions_2 = books_2 + chapters_2 + articles_2

            descriptions = descriptions_2

        # CASE 2.4: search1 without any operator (operator option == 'none') regardless of search2:
        else:
            books_1 = [obj for obj in books_1]
            chapters_1 = [obj for obj in chapters_1]
            articles_1 = [obj for obj in articles_1]
            descriptions_1 = books_1 + chapters_1 + articles_1
            descriptions = descriptions_1

    context = {
        'page_title': 'Wyszukiwanie',
        'results': sorted(descriptions, key=lambda desc: replace_special_chars(desc.description)),
        'is_searching': is_searching,
        'categories3': categories3,
        'categories': categories
    }
    return render(request, 'bibliography/bibliography_search.html', context)


def bibliography_reload_view(request):
    for obj in Book.objects.all():
        obj.save()
    for obj in Chapter.objects.all():
        obj.save()
    for obj in Article.objects.all():
        obj.save()

    for obj in CategoryLevelTwo.objects.all():
        obj.save()
    for obj in CategoryLevelThree.objects.all():
        obj.save()

    return redirect('bibliography:main')
