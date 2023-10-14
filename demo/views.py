from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse_lazy

from carInfo.models import Rental_Car, Selling_Car, Driver
from cusProfile.models import CusProfile
from payment.models import Rental_Car_payment, Sell_Car_Payment, Driver_Payment
from rentInfo.models import Rent_Car_Record
from sellInfo.models import Sell_Car_Record
from .form import CreateUserFrom, UserUpdateForm, ProfileUpdateForm, PasswordChangingForm


# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserFrom()

        if request.method == 'POST': #form theke data netese
            form = CreateUserFrom(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+ user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'registration.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')


        context = {}
        return render(request, 'login.html', context) #login hobe


def logoutUser(request):
    logout(request)
    return redirect('index')


class PasswordsChangeView(PasswordChangeView):

    form_class = PasswordChangingForm

    success_url = reverse_lazy('view-profile')



@login_required(login_url='login')
def editProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.cusprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('view-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.cusprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'edit-profile.html', context)



#profile information display er kaj korsi
@login_required(login_url='login')
def viewProfile(request):

    user_id = request.user
    pro_info = CusProfile.objects.filter(user=request.user).first()

    context={
        'user_id': user_id,
        'pro_info': pro_info

    }

    return render(request, 'userprofile.html', context)





#rent car gula display er kaj korsi
@login_required(login_url='login')
def rent_car(request):

    rentCar = Rental_Car.objects.all()

    return render(request, 'carrental.html', {'Rental_Cars': rentCar})





#car rent neyar jonno je je information lage oi page er kaj eikhane
@login_required(login_url='login')
def booking_details(request,pk,id):


    rentcars = Rental_Car.objects.filter(pk=pk).first()
    userid = User.objects.filter(id=id).first()
    contex = {
        'rentcars': rentcars,
    }


    if (request.method == 'POST'):

        rent_time = request.POST['rent_time']
        return_time = request.POST['return_time']
        pickup_loc = request.POST['pickup_loc']


        rentInfo = Rent_Car_Record(rent_time=rent_time, return_time=return_time, pickup_loc=pickup_loc, rent_car_id=rentcars, user_profile = userid)


        rentInfo.save()
        return redirect('/rent-payment-confirmation')

    return render(request, 'rentcardetails.html', contex)



#payment er transition id neyar kaj korsi
@login_required(login_url='login')
def rentPaymentconformation(request):

    rent_record = Rent_Car_Record.objects.all().last()
    rentcars = rent_record.rent_car_id.id
    userid = request.user.id
    car_image = rent_record.rent_car_id.car_image
    car_model = rent_record.rent_car_id.car_model



    contex = {
        'rent_record': rent_record,
        'car_image': car_image,
        'car_model': car_model
    }

    if (request.method == 'POST'):

        transition_id = request.POST['transition_id']


        rentPayment = Rental_Car_payment(rental_car_id=rentcars, user_profile_id=userid, transition_id=transition_id)


        rentPayment.save()
        return redirect('/home')


    return render(request, 'confirmation.html', contex )


#sell er gari gula display korar kaj korsi
@login_required(login_url='login')
def Buy_car(request):

    sellCar = Selling_Car.objects.all()

    return render(request, 'buycar.html',{'Selling_cars': sellCar})




#sell car gular details display korar kaj korsi
@login_required(login_url='login')
def car_details(request,pk,id):

    cars = Selling_Car.objects.filter(pk=pk).first()
    userid = User.objects.filter(id=id).first()
    contex= {
        'cars':cars
    }

    sellInfo = Sell_Car_Record(sell_car_id=cars, user_profile=userid)
    sellInfo.save()

    return render(request, 'cardetails.html',contex)



#sell car er order details & transition id nibo
@login_required(login_url='login')
def order_details(request,pk,id):
    buycars = Selling_Car.objects.filter(pk=pk).first()
    userid = User.objects.filter(id=id).first()
    contex = {
        'buycars': buycars,
    }

    if (request.method == 'POST'):
        transition_id = request.POST['transition_id']

        sellPayment = Sell_Car_Payment(sell_car_id=buycars, user_profile=userid, transition_id=transition_id)

        sellPayment.save()
        return redirect('/home')

    return render(request, 'buycarconfirmation.html',contex)

#driver display er kaj korsi
@login_required(login_url='login')
def driver(request):

    hireDriver = Driver.objects.all()

    return render(request, 'driver.html',{'Hire_Drivers': hireDriver})



#driver Payment er kaj korbo
@login_required(login_url='login')
def driver_payment(request,pk,id):
    drivers= Driver.objects.filter(pk=pk).first()
    userid = User.objects.filter(id=id).first()
    contex = {
        'drivers': drivers,
        'userid': userid
    }

    if (request.method == 'POST'):
        transition_id = request.POST['transition_id']

        driiverPayment = Driver_Payment(driver_id=drivers, user_profile=userid, transition_id=transition_id)

        driiverPayment.save()
        return redirect('/home')

    return render(request, 'driverpayment.html',contex)