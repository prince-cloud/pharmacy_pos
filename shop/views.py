from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Product, Purchase, ItemPurchase
from .forms import PurchaseForm, SupplyForm, ProductForm, ProductPurchaseForm
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created Successfully")
            redirect_url = request.GET.get("next")
            if redirect_url is not None:
                redirect(redirect_url)
    return redirect('items_list')

@login_required
def add_supply(request):
    if request.method == "POST":
        form = SupplyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supply created Successfully")
            redirect_url = request.GET.get("next")
            if redirect_url is not None:
                redirect(redirect_url)
        else:
            messages.error(request, "There was an error in the data entered")

    return redirect('items_list')


@login_required
def add_purchase(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()
            purchase_price = 0
            for item in json.loads(request.POST.get('json_product_list')):
                product = get_object_or_404(Product, pk=item.get('id'))
                quantity = int(item.get("quantity", 0))
                total_amount = float(product.price) * quantity
                purchase_price += total_amount
                
                ItemPurchase.objects.create(
                    purchase = purchase,
                    quantity = item.get("quantity", 0),
                    product = product,
                    total_amount = total_amount
                )
            purchase.total_amount = purchase_price
            purchase.save()

            messages.success(request, "Purchase created Successfully")
            redirect_url = request.GET.get("next")
            print(redirect_url, '\n\n')
            if redirect_url is not None:
                return redirect(redirect_url)
        else:
            messages.error(request, "There was an error in the data entered")
    return redirect('items_list')

@login_required
def history(request):
    purchases = Purchase.objects.all()
    return render(
        request, 
        'purchase_history.html', 
        {
            'purchases': purchases,
            'purchase_form': PurchaseForm(),
            'supply_form': SupplyForm(),
            'product_form': ProductForm(),
            'product_item_purchase_form': ProductPurchaseForm(),
        }
    )

@login_required
def items_list(request):
    items_list = Product.objects.all()
    
    search_query = request.GET.get('q')
    if search_query:
        items_list = items_list.filter(
            Q(name__icontains = search_query) |
            Q(description__icontains = search_query) 
        )

    return render(
        request,
        'items_list.html',
        {
            'products': items_list,
            'purchase_form': PurchaseForm(),
            'supply_form': SupplyForm(),
            'product_form': ProductForm(),
            'product_item_purchase_form': ProductPurchaseForm(),
        }
    )
