from celery import shared_task
from .models import BitcoinAddress, Transaction
from .services import BlockchainInfoAPI
from django.utils import timezone
from decimal import Decimal
import time

@shared_task
def sync_bitcoin_address(address_id, fetch_transactions=False, page_size=20, max_pages=5, reset_page=False):
    address = BitcoinAddress.objects.get(id=address_id)
    
    print(f"Starting synchronization for address: {address.address}")
    
    # Get address info from Blockchain.info
    info = BlockchainInfoAPI.get_address_info(address.address)
    
    if info:
        address.current_balance = info['balance']
        address.transaction_count = info['tx_count']
        # Save address info immediately
        address.save()
        print(f"Updated balance for {address.address}: {info['balance']} BTC")
        print(f"Transaction count: {info['tx_count']}")
        print(f"Address information saved to database")
    else:
        print(f"Failed to get address info for {address.address} from Blockchain.info API")
        
    # Only attempt to fetch transactions if explicitly requested
    if fetch_transactions:
        print(f"Attempting to fetch transactions for {address.address}")
        
        # Use pagination to fetch transactions in smaller batches
        total_fetched = 0
        new_transactions = 0
        
        # Reset page counter if requested or if we've fetched all transactions
        if reset_page or address.transaction_count <= Transaction.objects.filter(address=address).count():
            start_page = 0
            print(f"Starting from the first page (reset_page={reset_page})")
        else:
            # Start from the last fetched page
            start_page = address.last_fetched_page
            print(f"Continuing from page {start_page + 1}")
        
        for page_index in range(max_pages):
            page = start_page + page_index
            offset = page * page_size
            print(f"Fetching page {page+1} (offset={offset}, limit={page_size})")
            
            # Get transactions for this page
            transactions = BlockchainInfoAPI.get_transactions(address.address, limit=page_size, offset=offset)
            
            if not transactions:
                print(f"No more transactions found or rate limited at page {page+1}")
                break
                
            total_fetched += len(transactions)
            
            # Process transactions for this page
            for tx_data in transactions:
                tx_hash = tx_data['hash']
                # Skip if we already have this transaction
                if not Transaction.objects.filter(address=address, tx_hash=tx_hash).exists():
                    # Create new transaction
                    tx = Transaction(
                        address=address,
                        tx_hash=tx_hash,
                        amount=tx_data['amount'],
                        timestamp=tx_data['timestamp'],
                        is_sending=tx_data['is_sending'],
                        confirmations=tx_data.get('confirmations', 0)
                    )
                    tx.save()
                    new_transactions += 1
                    print(f"Added new transaction: {tx_hash}")
            
            print(f"Processed {len(transactions)} transactions from page {page+1}")
            
            # Update the last fetched page
            address.last_fetched_page = page + 1
            address.save()
            
            # If we got fewer transactions than requested, we've reached the end
            if len(transactions) < page_size:
                print(f"Reached end of transactions at page {page+1}")
                break
                
            # Add a delay between pages to avoid rate limiting
            if page_index < max_pages - 1:
                sleep_time = 30  # 30 seconds between pages
                print(f"Waiting {sleep_time} seconds before fetching next page...")
                time.sleep(sleep_time)
        
        print(f"Fetched a total of {total_fetched} transactions, added {new_transactions} new ones")
    else:
        print(f"Skipping transaction fetching as requested")
    
    # Update last sync time
    address.last_synced = timezone.now()
    address.save()
    
    print(f"Completed synchronization for address: {address.address}")
    return f"Synchronized {address.address}"