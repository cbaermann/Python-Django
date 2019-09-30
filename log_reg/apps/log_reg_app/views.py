from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Message, Comment

def index(request):
    return render(request, "log_reg_app/index.html")

def create_user(request):

     if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')


        new_user = User(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        )
        messages.success(request, "New user created")
        new_user.save()
        request.session["user"] = new_user.id
        request.session["first_name"] = new_user.first_name
        return redirect('/success')

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

    return redirect('/success')


def success(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "my_message": Message.objects.all()
    }
    return render(request, "log_reg_app/success.html", context)

def create_message(request):
    if request.method == "POST":
        new_message = Message(
            content = request.POST["message"],
            user = User.objects.get(id= request.session["user"])
        )
        new_message.save()
    return redirect("/success")

def delete_message(request, messageId):
    Message.objects.get(id=messageId).delete()
    return redirect('/success')

def create_comment(request, messageId):
    if request.method == "POST":
        new_comment = Comment(
            content = request.POST["comment"],
            message = Message.objects.get(id=messageId),
            user = User.objects.get(id = request.session["user"] )
        )
        new_comment.save()

    return redirect("/success")

def logout(request):
    request.session.clear()
    return redirect('/')


