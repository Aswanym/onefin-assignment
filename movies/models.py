import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movies(models.Model):

    uuid = models.UUIDField (default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField (max_length=225)
    description = models.CharField (max_length=225)
    genres = models.CharField(max_length=225)

    def __str__(self):
        return self.title

class Collection(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    movies = models.ManyToManyField(Movies, related_name='collections')

    def __str__(self):
        return self.title
