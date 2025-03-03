from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import BitcoinAddress, Transaction
from .forms import BitcoinAddressForm
from .tasks import sync_bitcoin_address

# Create your views here.

@login_required
def address_list(request):
    addresses = BitcoinAddress.objects.filter(user=request.user)
    return render(request, 'wallet/address_list.html', {'addresses': addresses})

@login_required
def address_detail(request, pk):
    address = get_object_or_404(BitcoinAddress, pk=pk, user=request.user)
    
    # Get all transactions for this address, ordered by timestamp (newest first)
    all_transactions = Transaction.objects.filter(address=address).order_by('-timestamp')
    
    # Set up pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(all_transactions, 25)  # Show 25 transactions per page
    
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        transactions = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        transactions = paginator.page(paginator.num_pages)
    
    return render(request, 'wallet/address_detail.html', {
        'address': address,
        'transactions': transactions,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': transactions
    })

@login_required
def add_address(request):
    if request.method == 'POST':
        form = BitcoinAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Bitcoin address added successfully!')
            return redirect('wallet:address_list')
    else:
        form = BitcoinAddressForm()
    return render(request, 'wallet/address_form.html', {'form': form})

@login_required
def remove_address(request, pk):
    address = get_object_or_404(BitcoinAddress, pk=pk, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Bitcoin address removed successfully!')
        return redirect('wallet:address_list')
    return render(request, 'wallet/address_confirm_delete.html', {'address': address})

@login_required
def sync_address(request, pk=None):
    # Get the fetch_transactions parameter from the query string
    fetch_transactions = request.GET.get('fetch_transactions', 'false').lower() == 'true'
    
    # Get the reset_page parameter from the query string
    reset_page = request.GET.get('reset_page', 'false').lower() == 'true'
    
    # Check if this is an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if pk:
        # Sync a single address
        address = get_object_or_404(BitcoinAddress, pk=pk, user=request.user)
        sync_bitcoin_address.delay(address.id, fetch_transactions=fetch_transactions, reset_page=reset_page)
        
        if not is_ajax:
            if fetch_transactions:
                if reset_page:
                    messages.info(request, f'Full synchronization started for {address.address} (starting from first page)')
                else:
                    messages.info(request, f'Full synchronization started for {address.address} (continuing from page {address.last_fetched_page + 1})')
            else:
                messages.info(request, f'Balance synchronization started for {address.address}')
            
            return redirect('wallet:address_detail', pk=pk)
        else:
            # For AJAX requests, return a simple 200 OK response
            from django.http import HttpResponse
            return HttpResponse(status=200)
    else:
        # Sync all addresses
        addresses = BitcoinAddress.objects.filter(user=request.user)
        for address in addresses:
            sync_bitcoin_address.delay(address.id, fetch_transactions=fetch_transactions, reset_page=reset_page)
        
        if not is_ajax:
            if fetch_transactions:
                if reset_page:
                    messages.info(request, f'Full synchronization started for {addresses.count()} addresses (starting from first page)')
                else:
                    messages.info(request, f'Full synchronization started for {addresses.count()} addresses (continuing from last page)')
            else:
                messages.info(request, f'Balance synchronization started for {addresses.count()} addresses')
        
            return redirect('wallet:address_list')
        else:
            # For AJAX requests, return a simple 200 OK response
            from django.http import HttpResponse
            return HttpResponse(status=200)
