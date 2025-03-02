from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    transactions = Transaction.objects.filter(address=address).order_by('-timestamp')
    return render(request, 'wallet/address_detail.html', {
        'address': address,
        'transactions': transactions
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
    if pk:
        # Sync a single address
        address = get_object_or_404(BitcoinAddress, pk=pk, user=request.user)
        sync_bitcoin_address.delay(address.id)
        messages.info(request, f'Synchronization started for {address.address}')
    else:
        # Sync all addresses
        addresses = BitcoinAddress.objects.filter(user=request.user)
        for address in addresses:
            sync_bitcoin_address.delay(address.id)
        messages.info(request, f'Synchronization started for {addresses.count()} addresses')
    
    return redirect('wallet:address_list')
