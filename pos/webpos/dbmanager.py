from django.contrib.auth.models import User
from webpos.models import Item, Bill, BillItem


def commit_bill(output, reqdata, user):
    billhd = Bill(customer_name=reqdata['customer_name'],
                  server=User.objects.get(pk=user.id).username)
    billitms = []
    reqquants = reqdata['items']
    dbitms = Item.objects.filter(name__in=reqquants.keys())

    for dbitm in dbitms:
        quant = reqquants[dbitm.name]
        db_quant = dbitm.quantity
        if db_quant is not None:
            newquant = db_quant - quant
            if newquant < 0:
                output['errors'].append((dbitm.name, dbitm.quantity))
            else:
                if output['errors']:
                    continue
                output['total'] += dbitm.price * quant
                billitms.append(BillItem(item=dbitm, quantity=quant,category=dbitm.category,
                                         item_price=dbitm.price))
                dbitm.quantity = newquant
        else:
            output['total'] += dbitm.price * quant
            billitms.append(BillItem(item=dbitm, quantity=quant,
                                     item_price=dbitm.price))

    if output['errors']:
        output['total'] = 0
        output['customer_id'] = None
        output['errors'] = dict(output['errors'])
        return output
    else:
        output['errors'] = dict(output['errors'])
        billhd.total = output['total']
        billhd.customer_id = output['customer_id']
        billhd.save()
        output['date'] = billhd.date
        output['bill_id'] = billhd.id
        for billitm, dbitm in zip(billitms, dbitms):
            billitm.bill = billhd
            billitm.save()
            dbitm.save()
        return output, billhd


def undo_bill(billid, user):
    bill = Bill.objects.get(pk=billid)
    if bill.deleted_by != '':
        return 'Bill has already been deleted!'
    for billitem in bill.billitem_set.all():
        billitem.item.quantity += billitem.quantity
        billitem.item.save()
    bill.deleted_by = user.username
    bill.save()
    return 'Bill #' + billid + ' deleted!'
