from django import forms
from .models import BitcoinAddress

class BitcoinAddressForm(forms.ModelForm):
    class Meta:
        model = BitcoinAddress
        fields = ['address', 'label']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bitcoin Address'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Label (optional)'})
        }

    def clean_address(self):
        address = self.cleaned_data['address']
        # Validation for different Bitcoin address formats
        
        # P2PKH addresses (start with 1) are 26-34 characters
        # P2SH addresses (start with 3) are 26-35 characters
        # Bech32 addresses (start with bc1) can be up to 90 characters
        
        if address.startswith('bc1'):
            # Bech32 address (native SegWit)
            if not (len(address) >= 14 and len(address) <= 90):
                raise forms.ValidationError("Invalid Bech32 address length")
        else:
            # Legacy address formats
            if not (len(address) >= 26 and len(address) <= 35):
                raise forms.ValidationError("Invalid Bitcoin address length")
                
        return address 