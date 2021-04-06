from django.contrib import admin
from .models import merch, brand, user_profile_info, order, banner, order_item

# Register your models here.
admin.site.register(brand)
admin.site.register(merch)
admin.site.register(user_profile_info)
admin.site.register(banner)


class order_item_inline(admin.TabularInline):
    model = order_item
    raw_id_fields = ['product']


class order_admin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [order_item_inline]


admin.site.register(order, order_admin)