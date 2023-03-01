from django.shortcuts import render,redirect

from .models import *
from .forms import *
from django.http import HttpResponse
# helpsto make multiple form with one filed
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import unauthanticated_user, authorized_user,admin_only


# Create your views here.
@unauthanticated_user
def register(request): 


    

     form = UserRegistrationForm()

     if request.method == 'POST':
     
         form = UserRegistrationForm(request.POST)
         if form.is_valid():
           user = form.save()
            # it will get username without the form fields
           username = form.cleaned_data.get('username')

           group = Group.objects.get(name='customer')
           user.groups.add(group)
           messages.success(request,f'Accounts was created for {username}')
         return redirect('/login')
            

     context={
        "form":form
     }
     return render (request,'accounts/register.html',context)



@unauthanticated_user
def loginpage(request):
     
    
            if request.method=='POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request,username= username,password=password)

                if user is not None:
                    login(request,user)
                    return redirect('home')
                else:
                    messages.info(request, 'Username or Password is incorrect')
                    
            
                
                
            return render (request,'accounts/login.html')
     


    
    
    #  if request.method=='POST':

    #   username = request.POST.get('username')
    #   password = request.POST.get('password')
    #   print(username, password)

    #   user = authenticate(request,username= username,password=password)

      

    #   if user is not None:
    #     login(request,user)
    #     return redirect('home')
      
    #   else:
    #    return HttpResponse("username password incorect")
          
    

def logoutUser(request):

    logout(request)

    return redirect('login')


      





@login_required(login_url='login')

@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()



    context = {"orders":orders,
               "customers": customers,
               "total_customers":total_customers,
               "total_orders":total_orders,
               "delivered":delivered,
               "pending":pending



               }
    
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
def customer (request,primarykey):
    customer = Customer.objects.get(id=primarykey)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilters = Orderfilters(request.GET, queryset=orders)
    orders = myFilters.qs


    context = {
        "customer":customer,
        "orders": orders,
        "order_count":order_count,
        "myFilters":myFilters,
    }

    return render(request,'accounts/customer.html',context)


@login_required(login_url='login')
@authorized_user(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    context ={
        'products':products
        }
    return render(request,'accounts/product.html',context)

@login_required(login_url='login')
@authorized_user(allowed_roles=['admin'])
def createorder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print("printhinf form data:", request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')




    context ={
        'formset':formset
    }


    return render(request,'accounts/orderForm.html',context)

# updateorder
@login_required(login_url='login')
@authorized_user(allowed_roles=['admin'])
def updateorder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # print("printhinf form data:", request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')




    context ={
        'form':form
    }

    return render (request,"accounts/orderForm.html",context)

@login_required(login_url='login')
@authorized_user(allowed_roles=['admin'])
def deleteorder(request,pk):
     order = Order.objects.get(id=pk)
     if request.method == "POST":
      order.delete()
      return redirect('/')

      
         

     context ={
        'item':order
    }
     return render (request,"accounts/deleteorder.html",context)





@login_required(login_url='login')
def createcustomer(request):
    form = CustomerForm
    if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
             form.save()
             return redirect('/')
    
    context ={
        'form':form
    }

    return render (request,"accounts/customerForm.html",context)



@login_required(login_url='login')
@authorized_user(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "total_orders":total_orders,
        "delivered":delivered,
        "pending":pending,
    }
    return render(request,'accounts/user.html',context)




@login_required(login_url='login')
@authorized_user(allowed_roles=['customer'])
def accountsetting(request):
    customer = request.user.customer
    form =CustomerForm(instance=customer) 

    if request.method == 'POST':
        form =CustomerForm(request.POST, request.FILES,instance=customer) 
        if form.is_valid():
            form.save()
            
    

    context={

        "form":form

    }

    return render (request,'accounts/accountsetting.html',context)

