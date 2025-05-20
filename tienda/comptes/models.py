from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TiendaUser(User):
    image = models.ImageField(default='imagesUsers/default.png', upload_to='imagesUsers/')
