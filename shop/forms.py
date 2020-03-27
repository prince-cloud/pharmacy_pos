from django import forms

from .models import Product, Supply, Purchase

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ('product', 'quantity')

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields  = ( 'customer', )
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields  = ('name', 'price', 'image')


class ProductPurchaseForm(forms.Form):
    try:
        CHOICES = list([(str(product.id), str(product)) for product in Product.objects.all()])
        CHOICES.insert(0, (-1,'NONE'))
    except Exception:
        CHOICES = [(-1, 'NONE')]
    product = forms.ChoiceField(choices = CHOICES)
    quantity = forms.CharField(widget=forms.NumberInput())