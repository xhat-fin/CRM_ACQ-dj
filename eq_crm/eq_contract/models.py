from django.db import models
from clients.models import Clients



class EqContracts(models.Model):
    contract_num = models.CharField(max_length=20, unique=True) #
    acc_num = models.CharField(max_length=28, unique=True) # f"BY{randint(10, 99)}HATN3819{randint(1000000000000000, 9999999999999999)}"
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    date_add = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    id_client = models.ForeignKey(Clients, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.contract_num}'



class EqTransactions(models.Model):
    contract = models.ForeignKey(EqContracts, on_delete=models.PROTECT)
    date_transaction = models.DateTimeField(auto_now_add=True)
    sum_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    num_card = models.CharField()
    sum_commission = models.DecimalField(max_digits=12, decimal_places=2)

    # мб удалю
    def save(self, *args, **kwargs):
        self.contract.balance += self.sum_transaction
        self.contract.commission += self.sum_commission
        self.contract.save()

        super().save(*args, **kwargs)
