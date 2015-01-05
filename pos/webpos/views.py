import json
from django.shortcuts import render_to_response#, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.views import generic
from django.db import transaction

from django.contrib.auth.models import User
from webpos.models import Item, Category, BillItem, Bill
from webpos import dbmanager as dbmng
from webpos.forms import ReportForm


def index(request):
    if request.user.is_authenticated():
        display_items = Item.objects.filter(enabled=True)
        server = User.objects.get(pk=request.user.id)
        return render_to_response('webpos/index.html', {'items': display_items,
                                                     'server': server})
    else:
        return HttpResponseRedirect(reverse('login'))


### AJAX REFRESH

# OUTPUT JSON
# {"item1": (quantity, price), ...}

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


def report(request):
    qs_empty = False    
    if request.GET:
        form = ReportForm(request.GET)
        if form.is_valid():
            sel_category = form.cleaned_data['sel_category']
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            qs = BillItem.objects.all().order_by('item__category', 'bill__date')
            if sel_category:
                qs = qs.filter(item__category=sel_category)
            if date_start:
                qs = qs.filter(bill__date__gte=date_start)
            if date_end:
                qs = qs.filter(bill__date__lte=date_end)            
            
            if not qs.exists():
                qs_empty = True
            return render_to_response('webpos/report.html', 
                                      {'form': form,
                                       'queryset': qs,
                                       'qs_empty': qs_empty})
        else:
            return render_to_response('webpos/report.html', 
                                      {'form': 'No!',
                                       'qs_empty': qs_empty})
    else:
        form = ReportForm()
        return render_to_response('webpos/report.html', 
                                  {'form': form,
                                   'qs_empty': qs_empty})


class BillDetailView(generic.DetailView):
    model = Bill
    template_name = 'webpos/bill_detail.html'
