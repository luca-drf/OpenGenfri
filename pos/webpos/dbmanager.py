from django.contrib.auth.models import User
from webpos.models import Item, Bill, BillItem


def commit_bill(output, reqdata, user):
    billhd = Bill(customer_name=reqdata['customer_name'],
                  server=User.objects.get(pk=user.id))
    billitms = []
    reqquants = reqdata['items']
    dbitms = Item.objects.filter(name__in=reqquants.keys())

    for dbitm in dbitms:
        quant = reqquants[dbitm.name]
        newquant = dbitm.quantity - quant
        if newquant < 0:
            output['errors'].append((dbitm.name, dbitm.quantity))
        else:
            if output['errors']:
                continue
            output['total'] += dbitm.price * quant
            billitms.append(BillItem(item=dbitm, quantity=quant,
                                     item_price=dbitm.price))
            dbitm.quantity = newquant

    if output['errors']:
        output['total'] = 0
        output['customer_id'] = None
        return output
    else:
        billhd.total = output['total']
        billhd.customer_id = output['customer_id']
        billhd.save()
        output['date'] = billhd.date
        output['bill_id'] = billhd.id
        for billitm, dbitm in zip(billitms, dbitms):
            billitm.bill = billhd
            billitm.save()
            dbitm.save()
        return output
