from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Branch)
admin.site.register(Package)
admin.site.register(ContactInfo)
admin.site.register(Ingredient)
admin.site.register(IngredientList)
