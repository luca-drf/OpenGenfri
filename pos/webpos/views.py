from django.shortcuts import render#, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django.views import generic
from django.contrib.auth.decorators import login_required

from webpos.models import Item


def index(request):
    if request.user.is_authenticated():
        display_items = Item.objects.filter(enabled=True)
        return render(request, 'webpos/index.html', {'items': display_items})
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def refresh_quantities(request):
    quantities = dict([(item.name, item.quantity)
                       for item in Item.objects.filter(enabled=True)])
    return JsonResponse(quantities)
