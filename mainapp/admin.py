from django.contrib import admin
from .models import Merch, Brand,UserProfileInfo,Order,Banner, OrderItem

# Register your models here.
admin.site.register(Brand)
admin.site.register(Merch)
admin.site.register(UserProfileInfo)
admin.site.register(Banner)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)