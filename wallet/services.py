import requests
from decimal import Decimal
from datetime import datetime
from .models import BitcoinAddress, Transaction

class BlockchairAPI:
    BASE_URL = "https://api.blockchair.com/bitcoin"
    
    @classmethod
    def get_address_info(cls, address):
        url = f"{cls.BASE_URL}/dashboards/address/{address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['data'][address]
            return {
                'balance': data['address']['balance'],
                'tx_count': data['address']['transaction_count']
            }
        return None
        
    @classmethod
    def get_transactions(cls, address):
        url = f"{cls.BASE_URL}/dashboards/address/{address}/transactions"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['data'][address]['transactions']
            transactions = []
            
            for tx in data:
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
                
                # Create transaction object
                transactions.append({
                    'hash': tx['hash'],
                    'amount': amount,
                    'timestamp': datetime.fromisoformat(tx['time']),
                    'confirmations': tx['confirmation_count'],
                    'is_sending': is_sending
                })
                
            return transactions
        return []