from django.contrib import admin
from webpos.models import Item, Category, Bill, BillItem, Location


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'category', 'quantity', 'priority',
                           'price', 'enabled']}),
    ]
    list_display = ('name', 'price', 'is_available', 'quantity', 'category',
                    'priority', 'enabled')
    search_fields = ['name', 'id']
    list_filter = ['category', 'enabled', 'quantity']


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'priority', 'enabled','printable']}),
    ]
    list_display = ('name', 'priority', 'enabled','enabled')
    search_fields = ['name']
    list_filter = ['enabled']


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['description', 'enabled']}),
    ]
    list_display = ('description', 'enabled')
    search_fields = ['description']
    list_filter = ['enabled']


class BillItemInline(admin.StackedInline):
    model = BillItem
    extra = 1


class BillAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['customer_name', 'customer_id', 'total', 'server',
            'deleted_by']})
    ]
    inlines = [BillItemInline]
    list_display = ('customer_name', 'customer_id', 'id', 'server', 'date',
            'total', 'is_committed')
    search_fields = ['customer_name', 'customer_id', 'id', 'date', 'server']


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Bill, BillAdmin)


