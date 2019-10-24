from django.shortcuts import render


def bibliography_main_view(request):
    context = {

    }
    return render(request, 'bibliography/bibliography_main.html', context)
