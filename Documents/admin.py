from django.contrib import admin
from .models import Product, ReceiptInvoice, ExpenditureInvoice
# Register your models here.


admin.site.register(Product)
admin.site.register(ReceiptInvoice)
admin.site.register(ExpenditureInvoice)