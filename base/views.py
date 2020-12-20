from django.shortcuts import render,redirect
from .models import User,Profile,SiteAnnouncement,Contact
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password
# Create your views here.
def home(request):
    announcement = SiteAnnouncement.objects.all()
    return render(request,"home.html",{'announcement':announcement})

def contact(request):
        if request.method=="POST":
            name=request.POST["cust_name"]
            email=request.POST["cust_email"]
            phone=request.POST["cust_mobile"]
            message=request.POST["cust_message"]
            Contact.objects.create(name=name,email=email,phone=phone,message=message)
            storage = messages.get_messages(request)
            storage.used = True
            msg = 'Mr. '+name+',\n\n\tThank you for joining with our Team. We will contact you soon'
            try:
                send_mail("SafeFarm Volunteer",msg,from_email='adityaintern11@gmail.com',recipient_list=[email])
            except Exception:
                messages.info(request,"Couldn't process your request now. Kindly try again later")
            else:
                messages.info(request,'Thank you for the request. Our Team will contact you soon')
        return redirect('/')

def register(request):
    if request.method=="POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        age = request.POST["age"]
        if int(age)<18 and int(age)>60:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Age Invalid. Age must be in 18-60')
            return redirect('/register')
        dob = request.POST['date_of_birth']
        address_lane_1 = request.POST["address_lane_1"]
        address_lane_2 = request.POST["address_lane_2"]
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        myfiles = request.FILES
        proof_of_residence = myfiles['proof_of_residence']
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        if len(mobile)!=10:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Invalid Mobile Number')
            return redirect('/register')
        alternate_phone = request.POST['alt_mobile']
        username = request.POST["username"]
        if len(User.objects.filter(username=username))>0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Username Already Taken')
            return redirect('/register')
        password = request.POST['password']
        confirm_password = request.POST['cnf_password']
        if password!=confirm_password:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Passwords Not Matching')
            return redirect('/register')
        profile_pic = myfiles['profile_pic']
        user_type = request.POST["user_type"]
        try:
            id = Profile.objects.create(age=age,dob=dob,photo=profile_pic,address_lane_1=address_lane_1,address_lane_2=address_lane_2,
                                landmark=landmark,city=city,state=state,pincode=pincode,alternate_phone=alternate_phone,proof_of_residence=proof_of_residence)
            User.objects.create_user(first_name=first_name,last_name=last_name,mobile=mobile,email=email,user_type=user_type,username=username,password=password,
                                user_profile=id)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'User Created Successfully.')
            return redirect('/')
        except Exception as e:
            print(e)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Try Again Later')
            return redirect('/')
    return render(request,'registration.html')

def login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        obj = authenticate(username=username,password=password)
        if obj is not None:
            auth.login(request,obj)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'User Login Successfully')
            if request.user.user_type=="Consumer":
                return redirect('/consumer/dashboard')
            elif request.user.user_type=="Producer":
                return redirect('/producer/dashboard') 
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Invalid Credentials')
    return redirect('/')

def logout(request):
    auth.logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Logged Out Successfully')
    return redirect('/')

def changeProfilePic(request):
    if request.method=="POST":
        urfiles = request.FILES
        photos = urfiles["pic"]
        obj = User.objects.get(username=request.user.username)
        obj2 = Profile.objects.get(id=obj.user_profile.id)
        obj2.photo = photos
        obj2.save(force_update=True)
        obj.save(force_update=True)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Profile Picture Updated Successfully')
        if request.user.user_type=="Customer":
            return redirect('/producer/home')
        elif request.user.user_type=="Worker":
            return redirect('/consumer/home') 

def changePassword(request):
    if request.method=="POST":
        username=request.POST["username"]
        obj = User.objects.get(username=username)
        number = random.randint(1000,9999)
        request.session["username"]=username
        request.session["otp_send"]=number
        msg = 'Hi '+obj.first_name+',\n\n\tOTP To change password: '+str(number)
        send_mail("GoHelp - Password Change",msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.email])
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'OTP Shared to your email id')
        return redirect('/validateOtp')
    return render(request,"startRecovery.html")

def validateOtp(request):
    if request.method=="POST":
        otp = request.POST["otp"]
        if int(otp)==int(request.session["otp_send"]):
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'OTP Verified. Provide New Password Credentials')
            return redirect('/setNewPassword')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'OTP Verification failed. Re-enter the username')
            return redirect('/changePassword')
    return render(request,'validateOtp.html')

def setNewPassword(request):
    if request.method=="POST":
        password=request.POST["new_password"]
        cnf_password=request.POST["cnf_password"]
        if password==cnf_password:
            password=make_password(password)
            obj = User.objects.get(username=request.session["username"])
            obj.password=password
            obj.save()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Password Changed Successfully')
            return redirect('/')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Passwords not matching')
            return redirect('/setNewPassword')
    return render(request,'setNewPassword.html')

def profile(request):
    if request.method=="POST":
        address_lane_1 = request.POST["address_lane_1"]
        address_lane_2 = request.POST["address_lane_2"]
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        myfiles = request.FILES
        proof_of_residence = myfiles['proof_of_residence']
        alternate_phone = request.POST['alt_mobile']
        obj = User.objects.get(username=request.user.username)
        obj2 = Profile.objects.get(id=obj.user_profile.id)
        obj2.address_lane_1,obj2.address_lane_2=address_lane_1,address_lane_2
        obj2.landmark=landmark
        obj2.city=city
        obj2.state=state
        obj2.pincode=pincode
        obj2.proof_of_residence=proof_of_residence
        obj2.alternate_phone=alternate_phone
        obj2.save(force_update=True)
        obj.save(force_update=True)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'User Profile Updated')
        if request.user.user_type=="Consumer":
            return redirect('/consumer/dashboard')
        elif request.user.user_type=="Producer":
            return redirect('/producer/dashboard')
    if request.user.user_type=="Consumer":
        return render(request,"consumer/profile.html")
    elif request.user.user_type=="Producer":
        return render(request,"producer/profile.html")
