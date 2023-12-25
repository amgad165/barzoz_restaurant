from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Menu_Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent_off', 'duration')
    # Exclude the stripe_coupon_id field from the admin page
    exclude = ('stripe_coupon_id',)

admin.site.register(Coupon, CouponAdmin)


admin.site.register(User_details)
