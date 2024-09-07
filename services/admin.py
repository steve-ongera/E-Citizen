from django.contrib import admin
from .models import *

admin.site.register(PublicRecord)
admin.site.register(MarriageLicense)
admin.site.register(PropertyDeed)
admin.site.register(Vehicle)
admin.site.register(Person)
admin.site.register(TaxPayment)

admin.site.register(Member)
admin.site.register(Month)
admin.site.register(MonthlyPayment)
