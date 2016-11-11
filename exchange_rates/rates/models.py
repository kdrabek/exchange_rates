from django.db import models


class Currency(models.Model):

    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    table_type = models.CharField(max_length=1)


class Rate(models.Model):

    code = models.ForeignKey('Currency')
    rate = models.DecimalField(max_digits=6, decimal_places=4)
    date = models.DateField(auto_now=False, auto_now_add=False)
    table_id = models.ForeignKey('Table')


class Table(models.Model):

    table_id = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=1)
    effective_date = models.DateField(auto_now=False, auto_now_add=False)
    when_fetched = models.DateTimeField(auto_now=False, auto_now_add=True)
