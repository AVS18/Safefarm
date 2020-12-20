from django.shortcuts import render,redirect
from producer.models import Product
from .models import Order
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.
def dashboard(request):
    return render(request,"consumer/dashboard.html")

def home(request):
    return render(request,'consumer/home.html')

def orderProduct(request):
    if request.method=="POST":
        pid=request.POST['pid']
        obj = Product.objects.get(id=pid)
        Order.objects.create(producer=obj.added_by,consumer=request.user,quantity=request.POST["quantity"],value=int(request.POST["quantity"])*int(obj.cost),status="Pending")
        try:
            msg = 'Greetings '+obj.added_by.first_name+',\n\n\tYou have received an order from a consumer. Kindly check your dashboard.'
            send_mail(subject="New Order Received -- Safeform",message=msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.added_by.email])
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Order Placed Successfully. Check your Past Orders for more details.')
        except Exception: 
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'There is a problem in the producer side. Kindly check your past order for more details')
        return redirect('/consumer/dashboard')
    return redirect('/consumer/catalogue')

def catalogue(request):
    product=Product.objects.all()
    return render(request,"consumer/catalogue.html",{'product':product})

def orders(request):
    obj = Order.objects.filter(consumer=request.user)
    return render(request,"consumer/orders.html",{'order':obj})