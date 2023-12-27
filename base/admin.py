from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Menu_Item)

admin.site.register(Category)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent_off', 'duration')
    # Exclude the stripe_coupon_id field from the admin page
    exclude = ('stripe_coupon_id',)

admin.site.register(Coupon, CouponAdmin)


# admin.site.register(User_details)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_summary', 'get_user_name', 'get_user_telefon', 'get_user_email',
                    'get_bezirk', 'get_street_address', 'get_hausnummer', 'get_plz_zip', 'get_city', 'ordered_date',
                    'get_total')


    def get_queryset(self, request):
        # Override get_queryset to include only orders where ordered = True
        return super().get_queryset(request).filter(ordered=True)

    def order_summary(self, obj):
        return ", ".join([f"{item.quantity} of {item.menu_item.name}" for item in obj.items.all()])
    order_summary.short_description = 'Order Summary'

    def get_user_name(self, obj):
        return obj.user_details.vorname + ' ' + obj.user_details.nachname if obj.user_details else ""
    get_user_name.short_description = 'Name'

    def get_user_telefon(self, obj):
        return obj.user_details.telefon if obj.user_details else ""
    get_user_telefon.short_description = 'Telefon'

    def get_user_email(self, obj):
        return obj.user_details.email if obj.user_details else ""
    get_user_email.short_description = 'Email'

    def get_bezirk(self, obj):
        return obj.user_details.bezirk if obj.user_details else ""
    get_bezirk.short_description = 'Bezirk'

    def get_street_address(self, obj):
        return obj.user_details.street_address if obj.user_details else ""
    get_street_address.short_description = 'Street Address'

    def get_hausnummer(self, obj):
        return obj.user_details.hausnummer if obj.user_details else ""
    get_hausnummer.short_description = 'Hausnummer'

    def get_plz_zip(self, obj):
        return obj.user_details.plz_zip if obj.user_details else ""
    get_plz_zip.short_description = 'PLZ/ZIP'

    def get_city(self, obj):
        return obj.user_details.city if obj.user_details else ""
    get_city.short_description = 'City'

    def um_hinweise(self, obj):
        return obj.user_details.um_hinweise if obj.user_details else ""
    um_hinweise.short_description = 'Um Hinweise'

    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total'

admin.site.register(Order, OrderAdmin)