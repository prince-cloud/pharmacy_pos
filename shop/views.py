from distutils.log import log
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
from django.utils import timezone
#from xhtml2pdf import pisa
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
def index(request):
    return render (request, 'index.html', 
    {
        'purchase_form': PurchaseForm(),
        'supply_form': SupplyForm(),
        'product_form': ProductForm(),
        'product_item_purchase_form': ProductPurchaseForm(),
        'expense_form': ExpenseForm(),
    })


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
    return redirect('inventory')


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
def add_supply(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = SupplyForm(request.POST)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.product = product
            form.save()
            messages.info(request, "Supply added Successfully")
            return redirect("/inventory/")
        else:
            messages.warning(request, "There was an error in the data entered")
    else:
        form = SupplyForm()

    return render(request, 'add_supply.html', {
        "form" : form,
        "product": product,
    })

@login_required
def sale(request):
    products = Product.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
        )

    return render(request, 'pos/sale.html', {
        "products": products,
    })


@login_required
def add_sale(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        if data is None:
            raise AttributeError

        purchase = Purchase.objects.create(
            total_amount=data['total_price'],
            seller = request.user
        )

        for order_item in data['order_list']:
            ItemPurchase(
                purchase = purchase,
                product=Product.objects.get(pk=order_item['id']),
                quantity=order_item['quantity'],
                total_amount=order_item['price'],
                seller=request.user
            ).save()
        purchase.save()
        messages.success(request, "Purchase successfully added")
        return redirect("/store/")
    return redirect("/store/")


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
        purchases = Purchase.objects.filter(date__date=timezone.now().date())
        expenses = Expense.objects.filter(date__date=timezone.now().date())

    total_purchases = 0
    total_expenses = 0
    for i in purchases:
        total_purchases += i.total_amount
    for x in expenses:
        total_expenses += x.amount
    
    net_total = total_purchases - total_expenses

    last_sales = 0
    for a in Purchase.objects.filter(date__gt=timezone.now() - datetime.timedelta(days=7)):
        last_sales += a.total_amount

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
            'last_sales': last_sales,
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

@login_required
def history_page(request):
    return render(request, 'history.html')

@login_required
def inventory(request):
    drugs = Product.objects.all()
    return render(request, 'inventory.html', {
        "drugs": drugs,
        'product_form': ProductForm(),
    })