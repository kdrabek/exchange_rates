from django.db import models


class Currency(models.Model):

    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    table_type = models.CharField(max_length=1)

    def __repr__(self):
        return '<Currency {0}>'.format(self.code)


class Rate(models.Model):

    currency = models.ForeignKey('Currency')
    rate = models.DecimalField(max_digits=6, decimal_places=4)
    table = models.ForeignKey('Table')

    def __repr__(self):
        return '<Rate currency: {0} table: {1}>'.format(
            self.currency.code, self.table.id)


class Table(models.Model):

    id = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=1)
    date = models.DateField(auto_now=False, auto_now_add=False)
    when_fetched = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __repr__(self):
        return '<Table id: {0} date: {1}>'.format(self.id, self.date)
