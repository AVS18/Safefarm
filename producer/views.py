from django.shortcuts import render,redirect
from .models import Product
from django.contrib import messages
from consumer.models import Order
from django.core.mail import send_mail

# Create your views here.
def dashboard(request):
    return render(request,"producer/dashboard.html")

def home(request):
    return render(request,'producer/home.html')

def addProduct(request):
    if request.method=="POST":
        name=request.POST["name"]
        myfiles = request.FILES
        image=myfiles["image"]
        ptype=request.POST["ptype"]
        quantity=request.POST["quantity"]
        ready_to_dispatch=request.POST["ready_to_dispatch"]
        usual_deliver_time=request.POST["usual_deliver_time"]
        Product.objects.create(name=name,image=image,ptype=ptype,quantity=quantity,ready_to_dispatch=ready_to_dispatch,usual_deliver_time=usual_deliver_time,added_by=request.user)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Product Created Successfully')
        return redirect('/producer/dashboard')
    return render(request,"producer/addProduct.html")

def updateProduct(request):
    if request.method=="POST":
        pid=request.POST["pid"]
        obj = Product.objects.get(id=pid)
        obj.quantity=request.POST["quantity"]
        obj.ready_to_dispatch=request.POST["ready_to_dispatch"]
        obj.usual_deliver_time=request.POST["usual_deliver_time"]
        obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Product Updated Successfully')
        return redirect('/producer/updateProduct')
    obj=Product.objects.filter(added_by=request.user)
    return render(request,"producer/updateProduct.html",{'product':obj})

def acceptOrder(request,id):
    obj = Order.objects.get(id=id)
    obj.status="Accepted"
    obj.save()
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Order Accepted')
    msg = 'Greetings '+obj.consumer.first_name+',\n\n\tYour Order is accepted. Check your dashboard'
    send_mail(subject="Order Accepted -- Safeform",message=msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.consumer.email])        
    return redirect('/producer/orders')

def rejectOrder(request,id):
    obj = Order.objects.get(id=id)
    obj.status="Rejected"
    obj.save()
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Order Rejected')
    msg = 'Greetings '+obj.consumer.first_name+',\n\n\tYour Order is rejected. Check your dashboard'
    send_mail(subject="Order Rejected -- Safeform",message=msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.consumer.email])
    return redirect('/producer/orders')

def orders(request):
    obj = Order.objects.filter(producer=request.user)
    return render(request,"producer/orders.html",{'order':obj})

def updateOrder(request,id):
    if request.method=="POST":
        tracking_id=request.POST["tracking_id"]
        courier_name=request.POST["courier_name"]
        exp_delivery=request.POST["exp_delivery"]
        status=request.POST["status"]
        obj = Order.objects.get(id=id)
        obj.tracking_id=tracking_id
        obj.status=status
        obj.courier_name=courier_name
        if exp_delivery!="":
            obj.exp_delivery=exp_delivery
        obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Order Updated Successfully')
        if status=="Rejected":
            msg = 'Greetings '+obj.consumer.first_name+',\n\n\tYour Order is rejected. Check your dashboard'
            send_mail(subject="Order Rejected -- Safeform",message=msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.consumer.email])
        elif status=="Dispatched":
            msg = 'Greetings '+obj.consumer.first_name+',\n\n\tYour Order is dispatched with tracking id as follows.'
            msg += '\nTracking Id:'+str(tracking_id)+'\nCourier Name:'+str(courier_name)+'\nCheck your dashboard for more details'
            send_mail(subject="Order Rejected -- Safeform",message=msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.consumer.email])
        elif status=="Accepted":
            msg = 'Greetings '+obj.consumer.first_name+',\n\n\tYour Order is accepted. Check your dashboard'
            send_mail(subject="Order Accepted -- Safeform",message=msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.consumer.email])        
        return redirect('/producer/orders') 
    obj = Order.objects.get(id=id)
    return render(request,"producer/updateOrder.html",{'obj':obj})