from django.shortcuts import render#, get_object_or_404
from django.http import JsonResponse#, HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.views import generic

from webpos.models import Item


def index(request):
    display_items = Item.objects.filter(enabled=True)
    return render(request, 'webpos/index.html', {'items': display_items})

def refresh_quantities(request):
    quantities = dict([(item.name, item.quantity)
                       for item in Item.objects.filter(enabled=True)])
    return JsonResponse(quantities)
