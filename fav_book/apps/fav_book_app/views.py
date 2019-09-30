from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User, Book

def index(request):
    return render(request, "fav_book_app/index.html")

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
        return redirect('/books')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.get(email= request.POST["email"])
        request.session["user"] = user.id
        request.session["first_name"] = user.first_name
    return redirect('/books')

def books(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id= request.session["user"]),
        "books": Book.objects.all()
    }
    return render(request, "fav_book_app/books.html", context)

def add_book(request, userId):

    if request.method == "POST":

        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')

        user = User.objects.get(id=userId)
        new_book = Book(
            title = request.POST["title"],
            description = request.POST["description"],
            uploaded_by = user
        )
        new_book.save()
        new_book.favorite.add(user)
    return redirect('/books')

def view_book(request, bookId):
    if "user" not in request.session:
        redirect('/')
    book = Book.objects.get(id = bookId)
    user = User.objects.get(id = request.session["user"])

    context = {
        "book": book, 
        "user": User.objects.get(id = request.session["user"])
    }

    return render(request, "fav_book_app/info.html", context)

def update_book(request, bookId):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        update_book = Book.objects.get(id=bookId)
        update_book.title = request.POST["title"] or update_book.title
        update_book.description = request.POST["description"] or update_book.description

        update_book.save()
        messages.success(request, f"{update_book.title} succesfully updated")

    return redirect('/books')

def add_favorites(request, bookId, userId):
    user = User.objects.get(id = userId)
    user.fav_book.add(Book.objects.get(id=bookId))

    return redirect('/books')

def remove_favorites(request, userId, bookId):
    user = User.objects.get(id= userId)
    user.fav_book.remove(Book.objects.get(id=bookId))
    
    return redirect(f"/books")


def delete(request, bookId):
    book = Book.objects.get(id=bookId)

    if book.uploaded_by.id != request.session["user"]:
        messages.error(request, "You do not have permission to remove this book")
        return redirect('/books')
    book.delete()
    messages.success(request, f"{book.title} successfully removed")
    return redirect('/books')


def logout(request):
    request.session.clear()
    return redirect('/')


# Create your views here.
