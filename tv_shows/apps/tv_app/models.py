from django.db import models

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["title"]) < 2:
            errors["title"] = "Title name should be at least 2 characters"
        if len(postData["network"]) < 3:
            errors["network"] = "Network name shoule be at least 3 characters"
        if len(postData["description"]) < 10:
            errors["description"] = "Description should be at least 10 characters"

        return errors
        

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=20)
    release = models.DateTimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

    def __repr__(self):
        return f"<Show object: {self.title} ({self.id})>"
    

# Create your models here.
