from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def log_view(request):
    context = {
        'page_title': 'Dziennik aktywności',
        'logs': LogEntry.objects.all(),
        'content_types_dict': {ct.id: ct for ct in ContentType.objects.all()}
    }
    return render(request, 'activity_log/log.html', context)
