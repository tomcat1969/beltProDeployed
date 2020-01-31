from django.shortcuts import render,redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request,"index.html")


def regist(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect("/")

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    hashed_PW = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = Users.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_PW,

    )
    print("add a user in datebase")
    request.session['id'] = user.id
    print("session id = ", request.session['id'])
    return redirect('/dashboard')

def login(request):
    if 'id' not in request:
        request.session['id'] = None
    user = Users.objects.filter(email=request.POST['email'])

    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['id'] = logged_user.id
            return redirect('/dashboard')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'id' not in request.session:
        print("you have to login")
        return redirect('/')
    logged_user = Users.objects.get(id=request.session['id'])
    trips_user_has = logged_user.trips.all()

    context = {
        "logged_user": logged_user,
        "trips_user_has":trips_user_has
    }
    return render(request,"dashboard.html",context)

def newtrip(request):
    if 'id' not in request.session:
        print("you have to login")
        return redirect('/')
    logged_user = Users.objects.get(id=request.session['id'])
    context = {
        "logged_user": logged_user,
    }
    return render(request,"newTrip.html")

def addNewTrip(request):
    errors = Trips.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect("/trips/new")

    destination = request.POST['destination']
    start_date_str = request.POST['start_date']
    start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")  ##show how to use datetime
    print(start_date_obj.strftime("%d %B, %Y"))

    end_date_str = request.POST['end_date']
    end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d")  ##show how to use datetime
    print(end_date_obj.strftime("%d %B, %Y"))

    plan = request.POST['plan']

    trip = Trips.objects.create(
        destination=destination,
        startDate=start_date_obj,
        endDate=end_date_obj,
        plan=plan,
        user_id=request.session['id']
    )
    print("add a trip in datebase",trip)

    return redirect('/dashboard')

def deleteTrip(request,trip_id):
    mytrip = Trips.objects.get(id=trip_id)
    mytrip.delete()
    return redirect('/dashboard')

def tripDetail(request,trip_id):
    if 'id' not in request.session:
        print("you have to login")
        return redirect('/')
    logged_user = Users.objects.get(id=request.session['id'])

    the_trip = Trips.objects.get(id=trip_id)
    context = {
        "logged_user": logged_user,
        "the_trip":the_trip
    }
    return render(request,"tripDetail.html",context)

def editTrip(request,trip_id):
    if 'id' not in request.session:
        print("you have to login")
        return redirect('/')
    logged_user = Users.objects.get(id=request.session['id'])
    
    the_trip = Trips.objects.get(id=trip_id)
    context = {
        "logged_user": logged_user,
        "the_trip": the_trip,
        "start_date":the_trip.startDate.strftime("%Y-%m-%d"),
        "end_date":the_trip.endDate.strftime("%Y-%m-%d")
    }
    return render(request,"editTrip.html",context)

def updateTrip(request):
    errors = Trips.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect("/trips/new")

    destination = request.POST['destination']
    start_date_str = request.POST['start_date']
    start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")  ##show how to use datetime
    print(start_date_obj.strftime("%d %B, %Y"))
    print("wwwww",start_date_obj.strftime("%Y-%m-%d"))
    end_date_str = request.POST['end_date']
    end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d")  ##show how to use datetime
    print(end_date_obj.strftime("%d %B, %Y"))

    plan = request.POST['plan']

    # trip = Trips.objects.create(
    #     #     destination=destination,
    #     #     startDate=start_date_obj,
    #     #     endDate=end_date_obj,
    #     #     plan=plan,
    #     #     user_id=request.session['id']
    #     # )
    print("11111")
    the_trip = Trips.objects.get(id=request.POST['trip_id'])
    the_trip.destination = destination
    the_trip.startDate = start_date_obj
    the_trip.endDate = end_date_obj
    the_trip.plan = plan
    the_trip.user_id = request.session['id']
    the_trip.save()
    print("update a trip in datebase", the_trip)

    return redirect('/dashboard')

