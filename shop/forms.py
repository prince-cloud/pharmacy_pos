from django import forms

from .models import Product, Supply, Purchase, Expense, ItemPurchase

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
        fields  = ('name', 'price','available_quantity', 'description')

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('description', 'amount')

class ProductPurchaseForm(forms.Form):
    
    product = forms.ChoiceField(choices = (), widget=forms.Select( attrs={'id': 'id_product_1'}))
    quantity = forms.CharField(widget=forms.NumberInput( attrs={'id': 'id_quantity_1'}))

    def __init__(self, *args, **kwargs):
        super(ProductPurchaseForm, self).__init__(*args, **kwargs)
        try:
            CHOICES = list([(str(product.id), str(product)) for product in Product.objects.all()])
            CHOICES.insert(0, (-1,'NONE'))
        except Exception as e:
            print('\n\n', e, '\n\n')
            CHOICES = [(-1, 'NONE')]
        self.fields['product'].choices = CHOICES

class GetItemForm(forms.ModelForm):
    class Meta:
        model = ItemPurchase
        fields = ('product',)