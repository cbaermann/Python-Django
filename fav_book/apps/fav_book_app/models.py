from __future__ import unicode_literals
from django.db import models
import bcrypt
from validate_email import validate_email

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters."

        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."

        if not validate_email(postData["email"]):
            errors["email"] = "Invalid email address"
        if User.objects.filter(email = postData["email"]):
            errors["inUserEmail"] = "Email address already in use"

        if len(postData["password"]) < 8:
            errors["password_length"] = "Password must be at least 8 characters."
        if postData["password"] != postData["confirm"]:
            errors["password"] = "Passwords do not match"

        return errors
    def login_validator(self, postData):
        errors = {}
        try : 
            user = User.objects.get(email = postData["email"])
        except:
            errors["email"] = f"No email adress matching {postData['email']}"
            return errors

        if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
            errors["password"] = "Password does not match email"
        return errors


class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}

        if len(postData["title"]) <1:
            errors["title"] = "Book must have a title"

        if len(postData["description"]) < 5:
            errors["description"] = "Book description must be at least 5 characters"
        return errors






class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User object: {self.first_name} ({self.last_name})>"


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name = "uploaded_book")
    favorite = models.ManyToManyField(User, related_name= "fav_book")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __repr__(self):
        return f"<Book object: {self.title} ({self.uploaded_by})>"



