from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices={"liqpay":"Pay with LiqPay", "monopay":"Pay with MonoPay", 
                                            "goggle pay":"Pay with Google Pay", "cash":"Pay with cash"})
    class Meta:
        model = Order
        fields = ["contact_name", "contact_email", "contact_phone", "address", "payment_method"]
        labels = {"contact_name": "Enter your name", 
                "contact_email" : "Enter your email",
                "contact_phone" : "Enter your phone", 
                "address" : "Enter your address",
                "payment_method" : "Payment Method"}
