import requests
import time
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from .models import BitcoinAddress, Transaction

class BlockchairAPI:
    """API for Bitcoin address information and transactions (requires API key for high usage)"""
    BASE_URL = "https://api.blockchair.com/bitcoin"
    API_KEY = getattr(settings, 'BLOCKCHAIR_API_KEY', '')
    RATE_LIMIT_DELAY = 60  # seconds between requests to respect the 1 request/minute average limit
    last_request_time = 0
    
    @classmethod
    def _respect_rate_limit(cls):
        """Add delay between requests to respect rate limit of 1440 requests per day (1 per minute avg)"""
        current_time = time.time()
        time_since_last_request = current_time - cls.last_request_time
        
        if cls.last_request_time > 0 and time_since_last_request < cls.RATE_LIMIT_DELAY:
            # Wait to respect rate limit
            sleep_time = cls.RATE_LIMIT_DELAY - time_since_last_request
            print(f"Rate limiting: Waiting {sleep_time:.2f} seconds before next Blockchair API request")
            time.sleep(sleep_time)
        
        cls.last_request_time = time.time()
    
    @classmethod
    def is_available(cls):
        """Check if this API is available (has API key for high usage or free tier for low usage)"""
        return True  # Always available, but will use API key if configured
    
    @classmethod
    def get_address_info(cls, address):
        cls._respect_rate_limit()
        url = f"{cls.BASE_URL}/dashboards/address/{address}"
        
        # Only add API key if it's configured
        params = {'key': cls.API_KEY} if cls.API_KEY else {}
        
        try:
            print(f"Fetching address info from Blockchair: {address}")
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()['data'][address]
                print(f"Successfully fetched info from Blockchair for address: {address}")
                # Convert satoshis to BTC
                balance_btc = Decimal(str(data['address']['balance'] / 100000000))
                return {
                    'balance': balance_btc,
                    'tx_count': data['address']['transaction_count']
                }
            elif response.status_code in [402, 429, 430, 434, 435, 503]:
                # These are rate limiting or API key related errors
                print(f"Blockchair API rate limit or key error: {response.status_code} - {response.text}")
                return None
            else:
                print(f"Blockchair API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error fetching address info from Blockchair: {str(e)}")
            return None
        
    @classmethod
    def get_transactions(cls, address):
        cls._respect_rate_limit()
        url = f"{cls.BASE_URL}/dashboards/address/{address}"
        
        # Only add API key if it's configured
        params = {'key': cls.API_KEY} if cls.API_KEY else {}
        
        try:
            print(f"Fetching transactions from Blockchair for address: {address}")
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()['data'][address]
                transactions_data = data.get('transactions', [])
                print(f"Successfully fetched {len(transactions_data)} transactions from Blockchair for address: {address}")
                transactions = []
                
                for tx in transactions_data:
                    # Determine if this is a sending or receiving transaction
                    is_sending = False
                    amount = Decimal('0')
                    
                    # Process inputs (sending)
                    for input_tx in tx['inputs']:
                        if input_tx['recipient'] == address:
                            is_sending = True
                            amount -= Decimal(str(input_tx['value'] / 100000000))  # Convert satoshis to BTC
                    
                    # Process outputs (receiving)
                    for output_tx in tx['outputs']:
                        if output_tx['recipient'] == address:
                            if not is_sending:  # Pure receiving transaction
                                amount += Decimal(str(output_tx['value'] / 100000000))  # Convert satoshis to BTC
                    
                    # Create transaction object with timezone-aware datetime
                    naive_timestamp = datetime.fromisoformat(tx['time'])
                    aware_timestamp = timezone.make_aware(naive_timestamp)
                    
                    # Create transaction object
                    transactions.append({
                        'hash': tx['hash'],
                        'amount': amount,
                        'timestamp': aware_timestamp,
                        'confirmations': tx['confirmation_count'],
                        'is_sending': is_sending
                    })
                    
                return transactions
            elif response.status_code in [402, 429, 430, 434, 435, 503]:
                # These are rate limiting or API key related errors
                print(f"Blockchair API rate limit or key error: {response.status_code} - {response.text}")
                return None
            else:
                print(f"Blockchair API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error fetching transactions from Blockchair: {str(e)}")
            return None


class BlockchainInfoAPI:
    """API for Bitcoin address information and transactions (no API key required)"""
    RATE_LIMIT_DELAY = 10  # seconds between requests to avoid rate limiting
    last_request_time = 0
    
    @classmethod
    def _respect_rate_limit(cls):
        """Add delay between requests to avoid rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - cls.last_request_time
        
        if cls.last_request_time > 0 and time_since_last_request < cls.RATE_LIMIT_DELAY:
            # Wait to respect rate limit
            sleep_time = cls.RATE_LIMIT_DELAY - time_since_last_request
            print(f"Rate limiting: Waiting {sleep_time:.2f} seconds before next Blockchain.info API request")
            time.sleep(sleep_time)
        
        cls.last_request_time = time.time()
    
    @classmethod
    def get_address_info(cls, address):
        cls._respect_rate_limit()
        try:
            print(f"Using Blockchain.info API for address info: {address}")
            # Use the simpler /balance endpoint instead of /address
            url = f"https://blockchain.info/balance?active={address}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"Successfully fetched info from Blockchain.info API for address: {address}")
                
                # The response format is different for this endpoint
                address_data = data.get(address, {})
                
                # Convert satoshis to BTC
                balance_btc = Decimal(str(address_data.get('final_balance', 0) / 100000000))
                
                return {
                    'balance': balance_btc,
                    'tx_count': address_data.get('n_tx', 0)
                }
            else:
                print(f"Blockchain.info API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error fetching address info from Blockchain.info API: {str(e)}")
            return None
    
    @classmethod
    def get_transactions(cls, address, limit=50, offset=0):
        try:
            print(f"Using Blockchain.info API for transactions: {address} (limit={limit}, offset={offset})")
            transactions = []
            
            # Implement retry with exponential backoff
            max_retries = 3
            retry_delay = 30  # Start with 30 seconds
            
            for retry in range(max_retries):
                if retry > 0:
                    print(f"Retry attempt {retry}/{max_retries} after waiting {retry_delay} seconds")
                    time.sleep(retry_delay)
                    # Double the delay for next retry (exponential backoff)
                    retry_delay *= 2
                
                # Respect rate limit before making the request
                cls._respect_rate_limit()
                
                url = f"https://blockchain.info/rawaddr/{address}?format=json&limit={limit}&offset={offset}"
                print(f"Making API request with limit={limit}, offset={offset}")
                
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    txs = data.get('txs', [])
                    
                    print(f"Successfully fetched {len(txs)} transactions from Blockchain.info API")
                    
                    if not txs:
                        return []
                    
                    for tx in txs:
                        # Determine if this is a sending or receiving transaction
                        is_sending = False
                        amount = Decimal('0')
                        
                        # Process inputs
                        for input_tx in tx['inputs']:
                            prev_out = input_tx.get('prev_out', {})
                            if prev_out.get('addr') == address:
                                is_sending = True
                                amount -= Decimal(str(prev_out.get('value', 0) / 100000000))  # Convert satoshis to BTC
                        
                        # Process outputs
                        for output in tx['out']:
                            if output.get('addr') == address:
                                if not is_sending:  # Pure receiving transaction
                                    amount += Decimal(str(output.get('value', 0) / 100000000))  # Convert satoshis to BTC
                        
                        # Create transaction object with timezone-aware datetime
                        timestamp = datetime.fromtimestamp(tx['time'])
                        aware_timestamp = timezone.make_aware(timestamp)
                        
                        transactions.append({
                            'hash': tx['hash'],
                            'amount': amount,
                            'timestamp': aware_timestamp,
                            'confirmations': data.get('confirmations', 0),
                            'is_sending': is_sending
                        })
                    
                    return transactions
                elif response.status_code == 429:
                    print(f"Rate limited (429). Will retry in {retry_delay} seconds.")
                    # Continue to next retry iteration
                else:
                    print(f"API Error: {response.status_code} - {response.text}")
                    # For non-rate-limit errors, don't retry
                    return []
            
            # If we've exhausted all retries
            print("Exhausted all retry attempts. Could not fetch transactions.")
            return []
        except Exception as e:
            print(f"Error fetching transactions from API: {str(e)}")
            return []


