from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.BinaryField()  # For storing image binary data
