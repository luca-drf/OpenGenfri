import json
import re
from decimal import Decimal
from easy_pdf.rendering import render_to_pdf_response
from django.shortcuts import render_to_response#, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.db.models import Q

from django.contrib.auth.models import User
from webpos.models import Item, Category, BillItem, Bill
from webpos import dbmanager as dbmng
from webpos.forms import ReportForm, SearchForm

from django.template import RequestContext

def index(request):
    """Testing view. If the request has an authenticated user token, the view
    returns a rendered page with all enabled items in the database and the
    username of the currently logged user. If the user is not authenticated it
    redirects to the login page."""
    if request.user.is_authenticated():
        display_items = Item.objects.filter(enabled=True)
        server = User.objects.get(pk=request.user.id)
        return render_to_response('webpos/index.html', {'items': display_items,
                                                     'server': server})
    else:
        return HttpResponseRedirect(reverse('login'))

def order(request):
    if request.user.is_authenticated():
        categories = Category.objects.filter(enabled=True).order_by('priority')
        items = Item.objects.filter(enabled=True).order_by('category','priority','name')
        return render_to_response('webpos/order.html', {
            'categories' : categories,
            'items'      : items
        })
    else:                                               # Daro: Lollo, ho
        return HttpResponseRedirect(reverse('login'))   # aggiunto questo caso
                                                        # per evitare di
                                                        # ritornare NULL in
                                                        # caso di utente non
                                                        # autenticato.

### AJAX REFRESH

# OUTPUT JSON
# {"item1": (quantity, price), ...}

@csrf_protect
def refresh_buttons(request):
    """Tentative view that should be polled by the client in order to refresh
    quantities and prices of the displayed buttons first created by index view"""
    if request.method == 'POST':# and request.is_ajax():
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
# { "errors": {},
#   "customer_id": customer_id,
#   "date": date,
#   "total": total
# }

@transaction.atomic
@csrf_protect # Daro: sarebbe figoso integrare CSRF token in questa POST
              # request
def bill_handler(request):
    """Called in order to commit a bill. The POST request must pass a json
    object structured as:

         { "customer_name": customer_name,
           "items": {
                "item1": {
                    "qty": quantity1,
                    "notes": "note1"
                }
                "item2": {
                    "qty": quantity2,
                    "notes": "note2"
                }
            }
         }

    Returning a json object of the form:
         
         { "errors": {},
           "customer_id": customer_id,
           "date": date,
           "total": total,
           "pdf_url": url
         }
    
    Where "errors" points to a dictionary having the names of the items that
    are no longer available as keys, and the actual database quantity of such
    item as value. If such dictionary is not empty the bill cannot be committed
    and it should be modified and reposted.
    """
    if request.method == 'POST':# and request.is_ajax():
        output = {'errors': [],
                  'bill_id': None,
                  'customer_id': '',
                  'date': None,
                  'total': 0,
                  'pdf_url': ''
                 }
        reqdata = json.loads(request.body)
        repdata, bill = dbmng.commit_bill(output, reqdata, request.user)
        if not repdata['errors']:
            repdata['pdf_url'] = reverse('webpos:pdf-bill', args=[bill.id])
        return JsonResponse(repdata)
    else:
        return HttpResponse(status=400)


def pdf_view(request, bill_id):
    bill = Bill.objects.get(pk=bill_id)
    items = bill.billitem_set.all()
    categories = Category.objects.all()
    billitems = {}
    headeritems = {}
    for cat in categories:
        itemlist = list(items.filter(category=cat)) 
        if itemlist:
            if cat.printable:
                billitems[cat] = itemlist
            headeritems[cat] = itemlist
    context = {'bill':bill, 'billitems':billitems, 'headeritems':headeritems}
    return render_to_pdf_response(request, 'webpos/comanda.html', context)


@transaction.atomic
@csrf_protect
def undo_bill(request):
    if request.POST.has_key('billid'):
        user = request.user
        billid = request.POST.get('billid', None)
        message = dbmng.undo_bill(billid, user)
        context = {'message': message}
        return JsonResponse(context)


def report(request, *args):
    """View that renders a report page to fetch all items sold under three
    constraints which are: Category, Begin Date/Time and End Date/Time."""
    if request.GET:
        form = ReportForm(request.GET)
        if form.is_valid():               
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            qs = Bill.objects.filter(deleted_by='')
            if date_start:
                qs = qs.filter(date__gte=date_start)
            if date_end:
                qs = qs.filter(date__lte=date_end)            
            
            if not qs.exists():
                return render_to_response('webpos/report.html', 
                                      {'form': form,
                                       #'report': None,
                                       'qs_empty': True})
            report_dict = {}
            for category in Category.objects.all():
                report_dict[category] = {'itemss': {}, 'items_sold': 0, 'total_price': Decimal(0.00)}
                for item in category.item_set.all():
                    report_dict[category]['itemss'][item] = {'quantity': 0,
                                                             'price': Decimal(0.00)}
            
            total_earn = Decimal(0)
            total_cash = Decimal(0)            
            for bill in qs:
                total_cash += bill.total
                
                for billitem in bill.billitem_set.all():
                    quantity = billitem.quantity
                    price = billitem.total_cost
                    entry_category = report_dict[billitem.category]
                    entry_category['items_sold'] += quantity
                    entry_category['total_price'] += abs(price)
                    entry_item = entry_category['itemss'][billitem.item]
                    entry_item['quantity'] += quantity
                    entry_item['price'] += abs(price)
                    if price > 0:
                        total_earn += price 
                

 
            return render_to_response('webpos/report.html', 
                                      {'form': form,
                                       'report': report_dict,
                                       'total_earn': total_earn,
                                       'total_cash': total_cash,
                                       #'qs_empty': False
                                       })
        else:
            return render_to_response('webpos/report.html', 
                                      {'form': 'Form Error!',
                                       #'qs_empty': qs_empty
                                       })
    else:
        form = ReportForm()
        return render_to_response('webpos/report.html', 
                                  {'form': form,
                                   #'qs_empty': qs_empty
                                   })


class BillDetailView(generic.DetailView):
    """Generic detail view to serve the bill_detail.html template"""
    model = Bill
    template_name = 'webpos/bill_detail.html'


def search(request, *args):
    """View that renders a simple search page that allow the user to find bills
    by customer name, server username or bill ID."""
    qs_empty = False
    if request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            qs = Bill.objects.all().filter(deleted_by='')
            search_text = form.cleaned_data['search']
            if re.match(r'\w+', search_text):
                qserver = Q(server__icontains=search_text)
                qcustomer = Q(customer_name__icontains=search_text)

                qs = qs.filter(qserver | qcustomer)
            
            elif re.match(r'\#([0-9]+)', search_text):
                number = re.match(r'\#([0-9]+)', search_text).group(1)
                qs = qs.filter(pk=int(number))

            if not qs.exists():
                qs_empty = True

            return render_to_response('webpos/search.html',
                                      {'form': form,
                                       'qs_empty': qs_empty,
                                       'queryset': qs},
                                      context_instance=RequestContext(request))

        else:
            return render_to_response('webpos/search.html',
                                      {'form': form,
                                       'qs_empty': qs_empty},
                                      context_instance=RequestContext(request))
    else:
        form = SearchForm()
        return render_to_response('webpos/search.html', {'form': form,
                                                         'qs_empty': qs_empty},
                                                         context_instance=RequestContext(request))

