from .models import New, Category


def latest_news(request):
    context = {
        'latest_news': New.objects.all().order_by('-publish_time')[:10],
        'categories': Category.objects.all(),
    }

    return context
