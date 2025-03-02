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
        # Basic validation for Bitcoin address format
        if not (len(address) >= 26 and len(address) <= 35):
            raise forms.ValidationError("Invalid Bitcoin address length")
        return address 