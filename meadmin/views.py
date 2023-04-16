from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitem=0
        birthdaycards=Product.objects.filter(category='B')
        lovecards=Product.objects.filter(category='L')
        paintings=Product.objects.filter(category='P')
        sistergifts=Product.objects.filter(category='S')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'home.html',{'birthdaycards':birthdaycards,'lovecards':lovecards,'paintings':paintings,'sistergifts':sistergifts,'totalitem':totalitem})


class ProductDeatilView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'productdetail.html', {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            totalamount=amount+shipping_amount
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
    else:
        return render(request,'emptycart.html',{'totalitem':totalitem})

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def buy_now(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'buynow.html',{'totalitem':totalitem})

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'orders.html',{'order_placed':op,'totalitem':totalitem})

def sistergift(request,data=None):
    totalitem=0
    if data==None:
        sistergifts=Product.objects.filter(category='S')
    elif data=='Bangle' or data=='Earring':
        sistergifts=Product.objects.filter(category='S').filter(brand=data)
    elif data=='below':
        sistergifts=Product.objects.filter(category='S').filter(discounted_price__lt=10000)
    elif data=='above':
        sistergifts=Product.objects.filter(category='S').filter(discounted_price__gt=10000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'sistergift.html',{'sistergifts':sistergifts,'totalitem':totalitem})

def painting(request,data=None):
    totalitem=0
    if data==None:
        paintings=Product.objects.filter(category='P')
    elif data=='Buddha' or data=='Mithila':
        paintings=Product.objects.filter(category='P').filter(brand=data)
    elif data=='below':
        paintings=Product.objects.filter(category='P').filter(discounted_price__lt=50000)
    elif data=='above':
        paintings=Product.objects.filter(category='P').filter(discounted_price__gt=50000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'painting.html',{'paintings':paintings,'totalitem':totalitem})

def lovecard(request,data=None):
    totalitem=0
    if data==None:
        lovecards=Product.objects.filter(category='L')
    elif data=='Anniversary' or data=='Girlfriend':
        lovecards=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        lovecards=Product.objects.filter(category='L').filter(discounted_price__lt=500)
    elif data=='above':
        lovecards=Product.objects.filter(category='L').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'lovecard.html',{'lovecards':lovecards,'totalitem':totalitem})

def birthdaycard(request,data=None):
    totalitem=0
    if data==None:
        birthdaycards=Product.objects.filter(category='B')
    elif data=='Circle' or data=='Heavy':
        birthdaycards=Product.objects.filter(category='B').filter(brand=data)
    elif data=='below':
        birthdaycards=Product.objects.filter(category='B').filter(discounted_price__lt=500)
    elif data=='above':
        birthdaycards=Product.objects.filter(category='B').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'birthdaycard.html',{'birthdaycards':birthdaycards,'totalitem':totalitem})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'customerregistration.html',{'form':form})
    
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'customerregistration.html',{'form':form})
        
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        totalamount=amount+shipping_amount
    totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')   

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
        
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            address=form.cleaned_data['address']
            reg=Customer(user=usr,name=name,address=address)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})


def contact(request):
    return render(request,'contactus.html')