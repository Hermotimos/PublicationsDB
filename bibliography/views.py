from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from bibliography.models import Book, Chapter, Article
from bibliography.utils import query_debugger
from categories.models import CategoryLevelOne, CategoryLevelTwo, CategoryLevelThree
from description_elements.models import Author, Translator, Location, Keyword, EncompassingBibliographicUnit, Periodical
from publications_db.utils import replace_special_chars


@query_debugger
def bibliography_full_view(request):
    books = [obj for obj in Book.objects.all()]
    chapters = [obj for obj in Chapter.objects.all()]
    articles = [obj for obj in Article.objects.all()]
    results = books + chapters + articles

    context = {
        'page_title': 'Pełna bibliografia',
        'results': sorted(results, key=lambda desc: replace_special_chars(desc.sorting_name)),
    }
    return render(request, 'bibliography/bibliography_full.html', context)


@query_debugger
def bibliography_index_view(request):
    categories1 = CategoryLevelOne.objects.all().prefetch_related('categories2__categories3')
    categories3 = CategoryLevelThree.objects.all().prefetch_related('books', 'chapters', 'articles')
    index = {}

    for cat3 in categories3:
        index[cat3] = [
            result for result in sorted(
                list(cat3.books.all())
                + list(cat3.chapters.all())
                + list(cat3.articles.all()),
                key=lambda result: replace_special_chars(result.sorting_name))
        ]

    context = {
        'page_title': 'Indeks tematyczny',
        'index': index,
        'categories1': categories1,

    }
    return render(request, 'bibliography/bibliography_index.html', context)


@query_debugger
def bibliography_search_view(request):
    is_searching = is_valid_search = False
    keywords_dict = {obj.id: obj.name for obj in Keyword.objects.all()}
    descriptions = []
    query_text = ''

    # text search
    search1 = request.GET.get('search1')
    search1 = search1.strip() if search1 else None
    if search1 and search1[0] == search1[-1] and search1[0] in ['"', '\'']:
        search1 = search1[1:-1]
    option1 = request.GET.get('option1')
    
    operator1 = request.GET.get('operator1')
    
    search2 = request.GET.get('search2')
    search2 = search2.strip() if search2 else None
    if search2 and search2[0] == search2[-1] and search2[0] in ['"', '\'']:
        search2 = search2[1:-1]
    option2 = request.GET.get('option2')

    # keywords search
    search3 = request.GET.get('search3')
    search3 = search3.strip() if search3 else None
    
    operator2 = request.GET.get('operator2')
    
    search4 = request.GET.get('search4')
    search4 = search4.strip() if search4 else None


    books_1 = Book.objects.all()
    books_2 = Book.objects.all()
    chapters_1 = Chapter.objects.all()
    chapters_2 = Chapter.objects.all()
    articles_1 = Article.objects.all()
    articles_2 = Article.objects.all()

    # TAB 1: TEXT SEARCH
    if request.GET.get('button1'):
        is_searching = True

        # CASE 1: invalid search i.e. search1 and search2 but no operator1 given:
        if search1 and search2 and operator1 == 'none':
            query_text = f'<b>Podano dwa warunki wyszukiwania, ale nie podano operatora logicznego.\n' \
                f'Wybierz operator logiczny, aby określić zależność między warunkami wyszukiwania.</b>'

        # CASE 2: invalid search i.e. search1 not empty and operator1 given but no search2 :
        elif search1 and operator1 != 'none' and not search2:
            query_text = f'<b>Podano jeden warunek wyszukiwania oraz operator logiczny, ' \
                f'ale nie podano drugiego warunku.\n' \
                f'Wybierając operator logiczny uzupełnij również drugi warunek wyszukiwania.</b>'

        # CASE 3: valid search i.e. search1 not empty and (operator1 and search2 are both either filled or empty):
        elif search1:
            is_valid_search = True
            option1_text = option2_text = ''

            # Preparation of search1 results:
            if option1 == 'all':
                books_1 = books_1.filter(description__icontains=search1)
                chapters_1 = chapters_1.filter(description__icontains=search1)
                articles_1 = articles_1.filter(description__icontains=search1)
                option1_text = 'Pełny opis'
            elif option1 == 'author':
                books_1 = books_1.filter(authors__last_name__icontains=search1)
                chapters_1 = chapters_1.filter(authors__last_name__icontains=search1)
                articles_1 = articles_1.filter(authors__last_name__icontains=search1)
                option1_text = 'Imię/nazwisko autora'
            elif option1 == 'editor':
                books_1 = books_1.filter(editors__last_name__icontains=search1)
                chapters_1 = chapters_1.filter(editors__last_name__icontains=search1)
                articles_1 = articles_1.none()
                option1_text = 'Imię/nazwisko redaktora'
            elif option1 == 'title':
                books_1 = books_1.filter(title__icontains=search1)
                chapters_1 = chapters_1.filter(title__icontains=search1)
                articles_1 = articles_1.filter(title__icontains=search1)
                option1_text = 'Tytuł'
            elif option1 == 'year':
                books_1 = books_1.filter(published_year__icontains=search1)
                chapters_1 = chapters_1.filter(published_year__icontains=search1)
                articles_1 = articles_1.filter(published_year__icontains=search1)
                option1_text = 'Rok wydania'

            # CASE 3.1: search1 and search2 and 'AND' operator1:
            if search1 and search2 and operator1 == 'and':
                if option2 == 'all':
                    books_2 = books_1.filter(description__icontains=search2)
                    chapters_2 = chapters_1.filter(description__icontains=search2)
                    articles_2 = articles_1.filter(description__icontains=search2)
                    option2_text = 'Pełny opis'
                elif option2 == 'author':
                    books_2 = books_1.filter(authors__last_name__icontains=search2)
                    chapters_2 = chapters_1.filter(authors__last_name__icontains=search2)
                    articles_2 = articles_1.filter(authors__last_name__icontains=search2)
                    option2_text = 'Imię/nazwisko autora'
                elif option1 == 'editor':
                    books_2 = books_1.filter(editors__last_name__icontains=search2)
                    chapters_2 = chapters_1.filter(editors__last_name__icontains=search2)
                    articles_2 = articles_1.none()
                    option2_text = 'Imię/nazwisko redaktora'
                elif option2 == 'title':
                    books_2 = books_1.filter(title__icontains=search2)
                    chapters_2 = chapters_1.filter(title__icontains=search2)
                    articles_2 = articles_1.filter(title__icontains=search2)
                    option2_text = 'Tytuł'
                elif option2 == 'year':
                    books_2 = books_1.filter(published_year__icontains=search2)
                    chapters_2 = chapters_1.filter(published_year__icontains=search2)
                    articles_2 = articles_1.filter(published_year__icontains=search2)
                    option2_text = 'Rok wydania'

                books = [obj for obj in books_2]
                chapters = [obj for obj in chapters_2]
                articles = [obj for obj in articles_2]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy spełniające oba warunki:</b> ' \
                    f'"{search1}" w polu "{option1_text}" ORAZ "{search2}" w polu "{option2_text}".'

            # CASE 3.2: search1 and search2 and 'OR' operator1:
            elif search1 and search2 and operator1 == 'or':
                if option2 == 'all':
                    books_2 = books_2.filter(description__icontains=search2).union(books_1)
                    chapters_2 = chapters_2.filter(description__icontains=search2).union(chapters_1)
                    articles_2 = articles_2.filter(description__icontains=search2).union(articles_1)
                    option2_text = 'Pełny opis'
                elif option2 == 'author':
                    books_2 = books_2.filter(authors__last_name__icontains=search2).union(books_1)
                    chapters_2 = chapters_2.filter(authors__last_name__icontains=search2).union(chapters_1)
                    articles_2 = articles_2.filter(authors__last_name__icontains=search2).union(articles_1)
                    option2_text = 'Imię/nazwisko autora'
                elif option2 == 'editor':
                    books_2 = books_2.filter(editors__last_name__icontains=search2).union(books_1)
                    chapters_2 = chapters_1.filter(editors__last_name__icontains=search2).union(chapters_1)
                    articles_2 = articles_1         # is equal to: articles_1.none().union(articles_1)
                    option2_text = 'Imię/nazwisko redaktora'
                elif option2 == 'title':
                    books_2 = books_2.filter(title__icontains=search2).union(books_1)
                    chapters_2 = chapters_2.filter(title__icontains=search2).union(chapters_1)
                    articles_2 = articles_2.filter(title__icontains=search2).union(articles_1)
                    option2_text = 'Tytuł'
                elif option2 == 'year':
                    books_2 = books_2.filter(published_year__icontains=search2).union(books_1)
                    chapters_2 = chapters_2.filter(published_year__icontains=search2).union(chapters_1)
                    articles_2 = articles_2.filter(published_year__icontains=search2).union(articles_1)
                    option2_text = 'Rok wydania'

                books = [obj for obj in books_2]
                chapters = [obj for obj in chapters_2]
                articles = [obj for obj in articles_2]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy spełniające co najmnniej jeden z dwóch warunków:</b> ' \
                    f'"{search1}" w polu "{option1_text}" LUB "{search2}" w polu "{option2_text}".'

            # CASE 3.3: search1 and search2 and 'AND NOT' operator1:
            elif search1 and search2 and operator1 == 'not':
                if option2 == 'all':
                    books_2 = books_1.exclude(description__icontains=search2)
                    chapters_2 = chapters_1.exclude(description__icontains=search2)
                    articles_2 = articles_1.exclude(description__icontains=search2)
                    option2_text = 'Pełny opis'
                elif option2 == 'author':
                    books_2 = books_1.exclude(authors__last_name__icontains=search2)
                    chapters_2 = chapters_1.exclude(authors__last_name__icontains=search2)
                    articles_2 = articles_1.exclude(authors__last_name__icontains=search2)
                    option2_text = 'Imię/nazwisko autora'
                elif option2 == 'editor':
                    books_2 = books_1.exclude(editors__last_name__icontains=search2)
                    chapters_2 = chapters_1.exclude(editors__last_name__icontains=search2)
                    articles_2 = articles_1       # is equal to articles_a.exclude()
                    option2_text = 'Imię/nazwisko redaktora'
                elif option2 == 'title':
                    books_2 = books_1.exclude(title__icontains=search2)
                    chapters_2 = chapters_1.exclude(title__icontains=search2)
                    articles_2 = articles_1.exclude(title__icontains=search2)
                    option2_text = 'Tytuł'
                elif option2 == 'year':
                    books_2 = books_1.exclude(published_year__icontains=search2)
                    chapters_2 = chapters_1.exclude(published_year__icontains=search2)
                    articles_2 = articles_1.exclude(published_year__icontains=search2)
                    option2_text = 'Rok wydania'

                books = [obj for obj in books_2]
                chapters = [obj for obj in chapters_2]
                articles = [obj for obj in articles_2]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy spełniające oba warunki:</b> ' \
                    f'"{search1}" w polu "{option1_text}" ORAZ BRAK "{search2}" w polu "{option2_text}".'

            # CASE 3.4: search1 and not search2 and not operator1:
            else:
                books = [obj for obj in books_1]
                chapters = [obj for obj in chapters_1]
                articles = [obj for obj in articles_1]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy spełniające warunek:</b> "{search1}" w polu "{option1_text}".'

    # TAB 2: KEYWORD SEARCH
    elif request.GET.get('button2'):
        is_searching = True

        # CASE 1: invalid search i.e. search3 and search4 but no operator2 given:
        if search3 and search4 and operator2 == 'none':
            query_text = f'<b>Wybrano dwa wyrażenia kluczowe, ale nie podano operatora logicznego.\n' \
                f'Wybierz operator logiczny, aby określić zależność między wyrażeniami kluczowymi.</b>'

        # CASE 2: invalid search i.e. search3 not empty and operator2 given but no search4 :
        elif search3 and operator2 != 'none' and not search4:
            query_text = f'<b>Wybrano jedno wyrażenie kluczowe oraz operator logiczny, ' \
                f'ale nie wybrano drugiego wyrażenia.\n' \
                f'Wybierając operator logiczny uzupełnij również drugie wyrażenie kluczowe.</b>'

        # CASE 3: valid search i.e. search1 not empty and (operator1 and search2 are both either filled or empty):
        elif search3:
            is_valid_search = True

            # Preparation of search3 results:
            books_1 = books_1.filter(keywords__name__icontains=search3)
            chapters_1 = chapters_1.filter(keywords__name__icontains=search3)
            articles_1 = articles_1.filter(keywords__name__icontains=search3)

            # CASE 3.1: search3 and search4 and 'AND' operator2:
            if search3 and search4 and operator2 == 'and':
                books_2 = books_1.filter(keywords__name__icontains=search4)
                chapters_2 = chapters_1.filter(keywords__name__icontains=search4)
                articles_2 = articles_1.filter(keywords__name__icontains=search4)

                books = [obj for obj in books_2]
                chapters = [obj for obj in chapters_2]
                articles = [obj for obj in articles_2]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy związane jednocześnie z dwoma wyrażeniami kluczowymi:</b> ' \
                    f'"{search3}" ORAZ "{search4}".'

            # CASE 3.2: search3 and search4 and 'OR' operator2:
            elif search3 and search4 and operator2 == 'or':
                books_2 = books_2.filter(keywords__name__icontains=search4).union(books_1)
                chapters_2 = chapters_2.filter(keywords__name__icontains=search4).union(chapters_1)
                articles_2 = articles_2.filter(keywords__name__icontains=search4).union(articles_1)

                books = [obj for obj in books_2]
                chapters = [obj for obj in chapters_2]
                articles = [obj for obj in articles_2]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy związane z jednym z dwóch wyrażeń kluczowych:</b> ' \
                    f'"{search3}" LUB "{search4}".'

            # CASE 3.3: search3 and search4 and 'AND NOT' operator2:
            elif search3 and search4 and operator2 == 'not':
                books_2 = books_1.exclude(keywords__name__icontains=search4)
                chapters_2 = chapters_1.exclude(keywords__name__icontains=search4)
                articles_2 = articles_1.exclude(keywords__name__icontains=search4)

                books = [obj for obj in books_2]
                chapters = [obj for obj in chapters_2]
                articles = [obj for obj in articles_2]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy związane związane z pierwszym wyrażeniem kluczowym, ' \
                    f'ale niezwiązane z drugim:</b> "{search3}" ORAZ "{search4}".'

            # CASE 3.4: search3 and not search4 and not operator2:
            else:
                books = [obj for obj in books_1]
                chapters = [obj for obj in chapters_1]
                articles = [obj for obj in articles_1]
                descriptions = books + chapters + articles

                query_text = f'<b>Wyszukaj opisy dla wyrażenia kluczowego:</b> "{search3}".'

    # NO FORM BY FIRST RENDERING OF bibliography_search.html PAGE
    else:
        pass

    context = {
        'page_title': 'Wyszukiwanie',
        'results': sorted(descriptions, key=lambda desc: replace_special_chars(desc.sorting_name)),
        'is_valid_search': is_valid_search,
        'is_searching': is_searching,
        'query_text': query_text,
        'keywords_dict': keywords_dict,
        'is_tab_2': search3,
    }
    return render(request, 'bibliography/bibliography_search.html', context)


@query_debugger
@login_required
def bibliography_reload_view(request):
    for obj in Book.objects.all():
        obj.save()
    for obj in Chapter.objects.all():
        obj.save()
    for obj in Article.objects.all():
        obj.save()

    for obj in CategoryLevelOne.objects.all():
        obj.save()
    for obj in CategoryLevelTwo.objects.all():
        obj.save()
    for obj in CategoryLevelThree.objects.all():
        obj.save()

    for obj in Author.objects.all():
        obj.save()
    for obj in Translator.objects.all():
        obj.save()
    for obj in Location.objects.all():
        obj.save()
    for obj in Keyword.objects.all():
        obj.save()

    for obj in EncompassingBibliographicUnit.objects.all():
        obj.save()
    for obj in Periodical.objects.all():
        obj.save()

    return redirect('bibliography:search')
