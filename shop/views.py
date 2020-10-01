from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Product, Purchase, ItemPurchase, Expense, Supply
from .forms import PurchaseForm, SupplyForm, ProductForm, ProductPurchaseForm, ExpenseForm, GetItemForm
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
import json
import datetime
from io import BytesIO
from django.template.loader import get_template
from django.http import FileResponse, HttpResponse
from xhtml2pdf import pisa
# Create your views here.

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}


@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Product Successfully added")
            redirect_url = request.GET.get("next")
            if redirect_url is not None:
                redirect(redirect_url)
    return redirect('items_list')


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(data=request.POST)
        if form.is_valid():
            expense = form.save()
            form.save()
            messages.info(request, 'Expense Successfully added')
            #if redirect_url is not None:
                #redirect(redirect_url)
    return redirect('history')


@login_required
def add_supply(request):
    if request.method == "POST":
        form = SupplyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Supply added Successfully")
            redirect_url = request.GET.get("next")
            if redirect_url is not None:
                redirect(redirect_url)
        else:
            messages.warning(request, "There was an error in the data entered")

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
                
                item_purchase = ItemPurchase.objects.create(
                    purchase = purchase,
                    quantity = item.get("quantity", 0),
                    product = product,
                    total_amount = total_amount
                )
            
            purchase.total_amount = purchase_price
            purchase.save()

            messages.info(request, "Item Successfully Purchased")
            redirect_url = request.GET.get("next")

            #if your want add printing
            #pdf = render_to_pdf('pdf_template.html', {'purchase': purchase})
            #return HttpResponse(pdf, content_type='application/pdf')
    
            if redirect_url is not None:
                return redirect(redirect_url)
        else:
            messages.warning(request, "There was an error in the data entered")
    return redirect('items_list')


@login_required
def history(request, year=None, month=None, day=None, drug=None):
    if year and month and day:
        purchases = Purchase.objects.filter(date__year=year, date__month=month, date__day=day)
        expenses = Expense.objects.filter(date__year=year, date__month=month, date__day=day)
    elif year and month:
        purchases = Purchase.objects.filter(date__year=year, date__month=month)
        expenses = Expense.objects.filter(date__year=year, date__month=month)
    elif year:
        purchases = Purchase.objects.filter(date__year=year)
        expenses = Expense.objects.filter(date__year=year)
    else:
        purchases = Purchase.objects.all()
        expenses = Expense.objects.all()

    total_purchases = 0
    total_expenses = 0
    for i in purchases:
        total_purchases += i.total_amount
    for x in expenses:
        total_expenses += x.amount
    
    net_total = total_purchases - total_expenses

    if drug:
        itempurchases = purchases.objects.filter(product=drug)

    return render(
        request, 
        'purchase_history.html', 
        {
            'purchases': purchases,
            'purchase_form': PurchaseForm(),
            'supply_form': SupplyForm(),
            'product_form': ProductForm(),
            'product_item_purchase_form': ProductPurchaseForm(),
            'expenses': expenses,
            'expense_form': ExpenseForm(),
            'year': year,
            'month': month,
            'day': day,
            'total_purchases': total_purchases,
            'total_expenses': total_expenses,
            'net_total': net_total,
            'drug': drug,
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
    items = Product.objects.all()
    items_json = [{'id': item.id,'name': item.name, 'quantity': item.available_quantity, 'price': float(item.price)} for item in items]
    
    return render(
        request,
        'items_list.html',
        {
            'products': items_list,
            'items': json.dumps(items_json),
            'purchase_form': PurchaseForm(),
            'supply_form': SupplyForm(),
            'product_form': ProductForm(),
            'product_item_purchase_form': ProductPurchaseForm(),
            'expense_form': ExpenseForm(),
        }
    )


@login_required
def drug_history(request, drug=None):
    products = None
    product_sold = 0
    qty = 0

    getDrug = ItemPurchase.objects.all()
    if drug:
        products = get_object_or_404(Product, name=drug)
        getDrug = getDrug.filter(products = products)

        

    search_query = request.GET.get('q')
    if search_query:
        getDrug = getDrug.filter(
            Q(product__name__icontains = search_query)
        )
        for i in getDrug:
            product_sold += i.total_amount
            qty += i.quantity
    

    return render(request, 'drug_history.html',
    {
        'getDrug': getDrug, 
        'products': products, 
        'product_sold': product_sold,
        'qty': qty,
    })


@login_required
def supply_history(request):
    supplies = Supply.objects.all()
    return render(request, 'supply_hisotry.html',
    {
        'supplies': supplies,
    })
