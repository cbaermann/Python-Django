from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Event
import datetime

def index(request):
    return render(request, "got_app/index.html")

def create_user(request):
    if request.method =="POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        )
        messages.success(request, "New user created")
        new_user.save()
        request.session["user"] = new_user.id
        request.session["first_name"] = new_user.first_name

        return redirect('/dashboard')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    user = User.objects.get(email = request.POST["email"])
    request.session["user"] = user.id
    request.session["first_name"] = user.first_name

    return redirect('/dashboard')

def dashboard(request):
    if "user" not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session["user"])
    context = {
        "user": user,
        "events": Event.objects.all(), 
        "times": len(user.attendent.all()),
        "created":len(user.creator.all()),
        "your_event": User.objects.get(id=user.id).attendent.all()
    }
    return render(request, "got_app/dashboard.html", context)

def shows(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "events" : Event.objects.all()
    }
    return render(request, "got_app/shows.html", context)

def new_show(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session["user"])
    }
    return render(request, "got_app/create.html", context)

def create_show(request, userId):
    if request.method == "POST":
        print(request.POST["title"])
        print(request.POST["location"])
        print(request.POST["date"])
        print(request.POST["genre"])

        user = User.objects.get(id=userId)
        add_show = Event.objects.create(
            title = request.POST["title"],
            location = request.POST["location"],
            date = request.POST["date"],
            genre = request.POST["genre"],
            creator = user,
        )
        add_show.attendent.add(user)
        add_show.save()

    return redirect('/dashboard')

def view(request, eventId):
    if "user" not in request.session:
        return redirect('/')
    event = Event.objects.get(id=eventId)
    context = {
        "event": event,
        "attendees": event.attendent.all()

    }
    return render(request, "got_app/view.html", context)

def join_event(request, eventId):
    user = User.objects.get(id=request.session["user"])
    event = Event.objects.get(id=eventId)
    event.attendent.add(user)
    event.save()

    return redirect('/shows')

def delete_event(request, eventId):
    event = Event.objects.get(id=eventId)

    if event.creator.id != request.session["user"]:
        messages.error(request, "You do not have permission to delete this event")
        return redirect('/shows')
    event.delete()

    return redirect('/shows')


def logout(request):
    request.session.clear()
    return redirect('/')

# Create your views here.
