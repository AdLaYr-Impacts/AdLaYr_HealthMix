from django import forms
from .models import UserAddress


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            "mobile_number",
            "address_line_1",
            "address_line_2",
            "address_line_3",
            "city",
            "district",
            "landmark",
            "pincode",
            "state",
        ]

        widgets = {
            'mobile_number': forms.TextInput(attrs={
                'required': 'required', 
            }),
            'address_line_1': forms.TextInput(attrs={
                'required': 'required', 
            }),
            'city': forms.TextInput(attrs={
                'required': 'required', 
            }),
            'district': forms.TextInput(attrs={
                'required': 'required', 
            }),
            'pincode': forms.TextInput(attrs={
                'required': 'required', 
            }),
            'state': forms.TextInput(attrs={
                'required': 'required', 
            }),
        }