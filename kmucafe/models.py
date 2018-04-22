from django.db import models

# Create your models here.

class Menu(models.Model):
    
    cafe1 = models.CharField(max_length=9999, default="")
    cafe2 = models.CharField(max_length=9999, default="")
    cafe3 = models.CharField(max_length=9999, default="")
    cafe4 = models.CharField(max_length=9999, default="")
    cafe5 = models.CharField(max_length=9999, default="")
    cafe6 = models.CharField(max_length=9999, default="1")
