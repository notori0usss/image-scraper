from django.db import models


# Create your models here.
class File(models.Model):
    docfile = models.FileField(upload_to='documents/%Y')
