from django.db.models import Sum
from datetime import date, timedelta
from .models import ReceiptInvoice, ExpenditureInvoice


def sales_report(start_date: date, end_date: date):
    """ця функція приймає два аргументи - початкову та кінцеву дату періоду, за який потрібно згенерувати звіт про
    продажі товарів. Функція повертає список словників, де кожен словник містить інформацію про окремий продукт та
    кількість його продажів за вказаний період."""
    sales = ReceiptInvoice.objects.filter(date__range=(start_date, end_date)).aggregate(Sum('transaction_value'))['transaction_value__sum']
    return sales or 0


def profit_report(start_date: date, end_date: date):
    """ця функція приймає два аргументи - початкову та кінцеву дату періоду, за який потрібно згенерувати звіт про
    прибутки. Функція повертає словник, де ключами є назви продуктів, а значеннями - прибутки, отримані з продажу цих
    продуктів за вказаний період."""
    sales = ReceiptInvoice.objects.filter(date__range=(start_date, end_date)).aggregate(Sum('transaction_value'))['transaction_value__sum']
    costs = ExpenditureInvoice.objects.filter(date__range=(start_date, end_date)).aggregate(Sum('transaction_value'))['transaction_value__sum']
    profit = (sales or 0) - (costs or 0)
    return profit


def stock_balance_report(as_of_date: date):
    """ця функція приймає один аргумент - дату, на яку потрібно згенерувати звіт про залишки товару. Функція повертає
    список словників, де кожен словник містить інформацію про окремий продукт та кількість його залишків на складі на
    вказану дату."""
    receipts = ReceiptInvoice.objects.filter(date__lte=as_of_date).aggregate(Sum('ending_quantity'))['ending_quantity__sum'] or 0
    expenditures = ExpenditureInvoice.objects.filter(date__lte=as_of_date).aggregate(Sum('ending_quantity'))['ending_quantity__sum'] or 0
    balance = receipts - expenditures
    return balance
