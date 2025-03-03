#!/usr/bin/env python
import os
import sys
import django
import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from wallet.services import BlockchainInfoAPI

# Temporarily increase the rate limit delay for testing
original_delay = BlockchainInfoAPI.RATE_LIMIT_DELAY
BlockchainInfoAPI.RATE_LIMIT_DELAY = 60  # Set to 60 seconds for testing

def test_get_address_info(address):
    """Test the get_address_info method with a given address"""
    print(f"\n=== Testing get_address_info for {address} ===")
    info = BlockchainInfoAPI.get_address_info(address)
    if info:
        print(f"Success! Address info retrieved:")
        print(f"Balance: {info['balance']} BTC")
        print(f"Transaction count: {info['tx_count']}")
        return True
    else:
        print(f"Failed to retrieve address info for {address}")
        return False

def test_get_transactions(address, limit=2):  # Reduced limit to 2
    """Test the get_transactions method with a given address"""
    print(f"\n=== Testing get_transactions for {address} (limit={limit}) ===")
    transactions = BlockchainInfoAPI.get_transactions(address, limit=limit)
    if transactions:
        print(f"Success! Retrieved {len(transactions)} transactions:")
        for i, tx in enumerate(transactions, 1):
            print(f"\nTransaction {i}:")
            print(f"Hash: {tx['hash']}")
            print(f"Amount: {tx['amount']} BTC")
            print(f"Timestamp: {tx['timestamp']}")
            print(f"Is sending: {tx['is_sending']}")
        return True
    else:
        print(f"Failed to retrieve transactions for {address}")
        return False

if __name__ == "__main__":
    # Use a Bitcoin address with fewer transactions
    test_address = "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ"
    
    # Allow command-line override of the test address
    if len(sys.argv) > 1:
        test_address = sys.argv[1]
    
    print(f"Testing BlockchainInfoAPI with address: {test_address}")
    print(f"Using increased rate limit delay of {BlockchainInfoAPI.RATE_LIMIT_DELAY} seconds")
    
    # Test get_address_info
    info_success = test_get_address_info(test_address)
    
    # Test get_transactions
    tx_success = test_get_transactions(test_address)
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"get_address_info: {'SUCCESS' if info_success else 'FAILED'}")
    print(f"get_transactions: {'SUCCESS' if tx_success else 'FAILED'}")
    
    if info_success and tx_success:
        print("\nAll tests passed! BlockchainInfoAPI is working correctly.")
    else:
        print("\nSome tests failed. BlockchainInfoAPI may not be working correctly.")
    
    # Restore original delay
    BlockchainInfoAPI.RATE_LIMIT_DELAY = original_delay 