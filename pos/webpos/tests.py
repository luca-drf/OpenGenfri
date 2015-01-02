from django.test import TestCase
from django.contrib.auth.models import User
from webpos.models import Item, Bill, BillItem, Category
from webpos.dbmanager import commit_bill


class BillTestCase(TestCase):
    def setUp(self):
        self.output = {'errors': [],
                       'bill_id': None,
                       'customer_id': 'LOL',
                       'date': None,
                       'total': 0
                      }
        bibite = Category.objects.create(name='Bibite')
        panini = Category.objects.create(name='Panini')
        piatti = Category.objects.create(name='Piatti')
        Item.objects.create(name='Coca Cola', category=bibite, quantity=11,
                            price=3.50)
        Item.objects.create(name='Panino Salsiccia', category=panini, 
                            quantity=0, price=6.50)
        Item.objects.create(name='Pasta al ragu', category=piatti, quantity=3,
                            price=8.50)
        Item.objects.create(name='Acqua', category=bibite, quantity=5,
                            price=1.00)
        User.objects.create(username='Lonfo')

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()
        User.objects.get(username='Lonfo').delete()

    def test_commit_bill_success(self):
        reqdata = {'customer_name': 'Darozzo',
                   'items': {'Coca Cola': 2,
                             'Pasta al ragu': 3,
                             'Acqua': 1
                            }
                }
        user = User.objects.get(username='Lonfo')
        result = commit_bill(self.output, reqdata, user)
        billhd = Bill.objects.get(pk=self.output['bill_id'])
        items = Item.objects.filter(name__in=reqdata['items'].keys())
        billitems = billhd.billitem_set.filter(item__in=items)

        for itm in billitems:
            self.assertEqual(itm.quantity, reqdata['items'][itm.item.name])
            self.assertEqual(itm.item_price, itm.item.price)

        self.assertTrue(len(billitems) == 3)
        self.assertEqual(billhd.customer_name, 'Darozzo')        
        self.assertEqual(billhd.server.username, 'Lonfo')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['customer_id'], 'LOL')
        self.assertEqual(result['total'], 33.5)

    def test_commit_bill_failure(self):
        reqdata = {'customer_name': 'Darozzo',
                   'items': {'Coca Cola': 2,
                             'Pasta al ragu': 4,
                             'Acqua': 6
                            }
                }
        user = User.objects.get(username='Lonfo')
        result = commit_bill(self.output, reqdata, user)
        
        self.assertTrue(len(result['errors']) == 2) 
        self.assertTrue(('Acqua', 5) in result['errors'])
        self.assertTrue(('Pasta al ragu', 3) in result['errors'])
        


