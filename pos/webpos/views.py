import json
from django.shortcuts import render#, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
# from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.contrib.auth.models import User
from webpos.models import Item, Category
from webpos import dbmanager as dbmng


def index(request):
    if request.user.is_authenticated():
        display_items = Item.objects.filter(enabled=True)
        server = User.objects.get(pk=request.user.id)
        return render(request, 'webpos/index.html', {'items': display_items,
                                                     'server': server})
    else:
        return HttpResponseRedirect(reverse('login'))

def order(request):
    if request.user.is_authenticated():
        categories = Category.objects.filter(enabled=True).order_by('priority')
        items = Item.objects.filter(enabled=True).order_by('category')
        return render(request, 'webpos/order.html', {
            'categories' : categories,
            'items'      : items
        })

### AJAX REFRESH

# OUTPUT JSON
# {"item1": (quantity, price), ...}

@login_required
def refresh_buttons(request):
    if request.is_ajax():
        items = dict([(item.name, (item.quantity, item.price))
                      for item in Item.objects.filter(enabled=True)])
        return JsonResponse(items)



### BILL MANAGMENT ################

# INPUT JSON
# { "customer_name": customer_name,
#   "items": {"item1": quantity,
#             "item2": quantity
#            }
# }

# OUTPUT JSON
# { "errors": [],
#   "customer_id": customer_id,
#   "date": date,
#   "total": total
# }

@login_required
@transaction.atomic
#@csrf_protect
def bill_handler(request):
    if request.method == 'POST' and request.is_ajax():
        output = {'errors': [],
                  'bill_id': None,
                  'customer_id': 'LOL',
                  'date': None,
                  'total': 0
                 }
        reqdata = json.loads(request.body)
        return JsonResponse(dbmng.commit_bill(output, reqdata, request.user))


