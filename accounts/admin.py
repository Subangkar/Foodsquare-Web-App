from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)

admin.site.register(Restaurant)
admin.site.register(RestaurantBranch)

admin.site.register(Delivery)
admin.site.register(DeliveryMan)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderPackageList)
