from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
PRODUCT_TYPE = [
    ("Product", "Продукт"),
    ("Service", "Послуга")
]


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    is_service = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def update_quantity(self, quantity_change):
        self.quantity += quantity_change
        self.save()


class ReceiptInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    product = models.CharField(max_length=100, name="Neme product")
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE)
    starting_quantity = models.IntegerField(help_text="кількість продуктів на складі до транзакції")
    ending_quantity = models.IntegerField(help_text="кількість продуктів на складі після транзакції")
    transaction_value = models.IntegerField("вартість всіх продуктів у транзакції")

    def validate_stock_availability(self):
        if self.starting_quantity > self.product.quantity:
            raise ValidationError('На складі недостатньо товару!')
        else:
            return True

    def save(self, *args, **kwargs):
        self.validate_stock_availability()
        product = Product.objects.get(name=self.product)
        product.update_quantity(self.starting_quantity - self.ending_quantity)
        super(ExpenditureInvoice, self).save(*args, **kwargs)


class ExpenditureInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    product = models.CharField(max_length=100, name="Neme product")
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE)
    starting_quantity = models.IntegerField(help_text="кількість продуктів на складі до транзакції")
    ending_quantity = models.IntegerField(help_text="кількість продуктів на складі після транзакції")
    transaction_value = models.IntegerField("вартість всіх продуктів у транзакції")

    # З наслідуванням були помилки тому виконав так

    def validate_stock_availability(self):
        if self.starting_quantity > self.product.quantity:
            raise ValidationError('На складі недостатньо товару!')
        else:
            return True

    def save(self, *args, **kwargs):
        """Таким чином, при створенні накладної або рахунку буде оновлюватись кількість продуктів на складі відповідно до
        типу транзакції та згідно з методом FIFO."""
        self.validate_stock_availability()
        product = Product.objects.get(name=self.product)
        product.update_quantity(self.starting_quantity - self.ending_quantity)
        super(ExpenditureInvoice, self).save(*args, **kwargs)


