from django.db import models
from django.conf import settings

class BitcoinAddress(models.Model):
    address = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_synced = models.DateTimeField(null=True, blank=True)
    current_balance = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bitcoin_addresses')

class Transaction(models.Model):
    tx_hash = models.CharField(max_length=100, unique=True)
    address = models.ForeignKey(BitcoinAddress, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=30, decimal_places=8)
    timestamp = models.DateTimeField()
    confirmations = models.IntegerField(default=0)
    is_sending = models.BooleanField()  # True if sending, False if receiving