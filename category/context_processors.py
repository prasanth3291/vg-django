from.models import category,Sub_category

def menu_links(request):
    links=category.objects.all()
    links1=Sub_category.objects.all()
    
    return dict(links=links,links1=links1)