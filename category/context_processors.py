from .models import category, Sub_category
from store.models import Size


def menu_links(request):
    links = category.objects.all()
    links1 = Sub_category.objects.all()
    chart = Size.objects.all()

    return dict(links=links, links1=links1, chart=chart)
