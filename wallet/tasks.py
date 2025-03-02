from celery import shared_task
from .models import BitcoinAddress, Transaction
from .services import BlockchairAPI
from django.utils import timezone
from decimal import Decimal

@shared_task
def sync_bitcoin_address(address_id):
    address = BitcoinAddress.objects.get(id=address_id)
    
    # Get address info
    info = BlockchairAPI.get_address_info(address.address)
    if info:
        address.current_balance = info['balance']
        
    # Get and store transactions
    transactions = BlockchairAPI.get_transactions(address.address)
    if transactions:
        for tx_data in transactions:
            # Check if transaction already exists
            tx, created = Transaction.objects.get_or_create(
                tx_hash=tx_data['hash'],
                address=address,
                defaults={
                    'amount': Decimal(tx_data['amount']),
                    'timestamp': tx_data['timestamp'],
                    'confirmations': tx_data['confirmations'],
                    'is_sending': tx_data['is_sending']
                }
            )
            
            # Update confirmations for existing transactions
            if not created and tx.confirmations != tx_data['confirmations']:
                tx.confirmations = tx_data['confirmations']
                tx.save()
    
    address.last_synced = timezone.now()
    address.save()
    
    return f"Synchronized {address.address}"