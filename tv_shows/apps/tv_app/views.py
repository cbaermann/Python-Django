from django.shortcuts import render, redirect
from .models import Show
from django.contrib import messages

def index(request):
    return redirect('/shows')

def shows(request):
    context = {"shows": Show.objects.all()}
    return render(request, "tv_app/index.html", context)

def new_show(request):
    return render(request, "tv_app/new_show.html")

def show_id(request, showId):
    context = {"show": Show.objects.get(id=showId),
    }

    return render(request, "tv_app/show_id.html", context)


def create_show(request):
    if request.method == "POST":
        errors = Show.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/shows/new')
        
        else:

            new_show = Show.objects.create(
                title = request.POST["title"],
                network = request.POST["network"],
                release = request.POST["release"],
                description = request.POST["description"],
            )
            new_show.save()
    return redirect(f"/shows/{new_show.id}")

def edit(request, showId):
    context = {"show": Show.objects.get(id=showId),
    }
    
    return render(request, "tv_app/edit_show.html", context)

def edit_show(request, showId):
    if request.method == "POST":
        errors = Show.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/shows/new')
        else:
            edit_show = Show.objects.get(id=showId)
            edit_show.title = request.POST["title"] or edit_show.title
            edit_show.description = request.POST["description"] or edit_show.description
            edit_show.network = request.POST["network"] or edit_show.network
            edit_show.release = request.POST["release"] or edit_show.release
            edit_show.save()

    return redirect(f"/shows/{edit_show.id}")


def destroy(request, showId):
    delShow = Show.objects.get(id = showId)
    delShow.delete()

    return redirect("/shows")

# Create your views here.
