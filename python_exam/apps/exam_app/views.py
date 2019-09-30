from django.shortcuts import render, redirect 
import bcrypt
from django.contrib import messages
from .models import User, Job
import datetime

def index(request):
    return render(request, "exam_app/index.html")

def create_user(request):
    if request.method == "POST":
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
     if request.method =="POST":
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
    context = {
        "jobs": Job.objects.all()
    }
    return render(request, "exam_app/dashboard.html", context)

def new_job(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session["user"])
    }
    return render(request, "exam_app/newjob.html", context)

def create_job(request, userId):
    if request.method == "POST":
        errors = Job.objects.event_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new_job')
        user = User.objects.get(id=userId)
        add_job = Job.objects.create(
            title = request.POST["title"],
            description = request.POST["description"],
            location = request.POST["location"],
            creator = user,
        )
        add_job.save()
        return redirect('/dashboard')

def view_job(request, jobId):
    if "user" not in request.session:
        return redirect('/')
    job = Job.objects.get(id=jobId)
    context = {
        "job": job
    }

    return render(request, "exam_app/view.html", context)

def edit_job(request, jobId):
    if "user" not in request.session:
        return redirect('/')
    job = Job.objects.get(id=jobId)
    user = User.objects.get(id= request.session["user"])

    context = {
        "job": job,
        "user": user
    }
    return render(request, "exam_app/edit_job.html", context)

def update_job(request, jobId):
    if request.method == "POST":
        errors = Job.objects.event_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit/'+jobId+'')

        update_job = Job.objects.get(id=jobId)
        update_job.title = request.POST["title"] or update_job.title
        update_job.description = request.POST["description"] or update_job.description
        update_job.location = request.POST["location"] or update_job.location
        update_job.save()

        return redirect('/dashboard')
        


def remove_job(request, jobId):
    job = Job.objects.get(id=jobId)
    if "user" not in request.session:
        return redirect('/')
    if job.creator.id != request.session["user"]:
        messages.error(request, "You do not have permission to delete this job")
        return redirect('/')
    job.delete()
    return redirect('/dashboard')

def cancel(request):
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')


# Create your views here.
