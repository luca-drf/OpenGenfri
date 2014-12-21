from django.db import models

# Location class, used to determine from wich actual pos location the cashier is working (ex. Bar, restaurant, ...)

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)
    enabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

# Category class, used as a container for different type of items, related by area (ex. Kitchen, beverages, ...)

class Category(models.Model):
    id = models.Autofiled(primary_key=True)
    name = models.CharField(max_length=30)
   # location = models.ForeignKey('Location')
    priority = models.PositiveSmallIntegerField()
    enabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

# Item class, basically the items that we'll sell (ex. Coke, Pizza, Costata, ...)

class Item(models.Model):
    id = models.Autofiled(primary_key=True) #check if ID is useful
    name = models.CharField(max_length=30)
    category = models.ForeignKey('Category')
    quantity = models.PositiveSmallIntegerField()
    priority = models.PositiveSmallIntegerField()
    enabled = models.BooleanField(default=False)
    price = models.IntegerField()

# Bill class, it stores a whole order made by one client 

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=40)
    total = models.FloatField()

# class to store the single entries that when grouped together will form one, and just one bill

class BillItem(models.Model):
    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey('Bill')
    item = models.ForeignKey('Item')
    quantity = models.PositiveSmallIntegerField()
    total = models.IntegerField()
