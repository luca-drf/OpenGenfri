import json
import re
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
from easy_pdf.views import PDFTemplateView

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
        items = Item.objects.filter(enabled=True).order_by('category')
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
           "items": {"item1": quantity,
                     "item2": quantity
                    }
         }

    Returning a json object of the form:
         
         { "errors": {},
           "customer_id": customer_id,
           "date": date,
           "total": total
         }
    
    Where "errors" points to a dictionary having the names of the items that
    are no longer available as keys, and the actual database quantity of such
    item as value. If such dictionary is not empty the bill cannot be committed
    and it should be modified and reposted.
    """
    if request.method == 'POST':# and request.is_ajax():
        output = {'errors': [],
                  'bill_id': None,
                  'customer_id': 'LOL',
                  'date': None,
                  'total': 0
                 }
        reqdata = json.loads(request.body)
        repdata = dbmng.commit_bill(output, reqdata, request.user)
        if repdata['errors']:
            return JsonResponse(repdata)
        # else:
        #     return render_to_pdf_response(request,
        #                                   'webpos/pdf_template.html',
        #                                   reqdata)
    else:
        return HttpResponse('asyvbasvbayvasouvo')


def pdf_view(request):
    bill = Bill.objects.get(customer_name='fedfol')
    items =bill.billitem_set.all()
    categories = Category.objects.all()
    billitems = {}
    for cat in categories:
        itemlist = list(items.filter(category=cat)) 
        if itemlist:
            billitems[cat] = itemlist
    context = {'bill':bill, 'billitems':billitems}
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
    qs_empty = False    
    if request.GET:
        form = ReportForm(request.GET)
        if form.is_valid():
            sel_category = form.cleaned_data['sel_category']
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            qs = BillItem.objects.all().filter(bill__deleted_by='')
            qs = qs.order_by('item__category', 'bill__date')
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
                                      {'form': 'Form Error!',
                                       'qs_empty': qs_empty})
    else:
        form = ReportForm()
        return render_to_response('webpos/report.html', 
                                  {'form': form,
                                   'qs_empty': qs_empty})


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
                qserver = Q(server__contains=search_text)
                qcustomer = Q(customer_name__contains=search_text)

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
                                      {'form': 'No!',
                                       'qs_empty': qs_empty},
                                      context_instance=RequestContext(request))
    else:
        form = SearchForm()
        return render_to_response('webpos/search.html', {'form': form,
                                                         'qs_empty': qs_empty},
                                                         context_instance=RequestContext(request))

