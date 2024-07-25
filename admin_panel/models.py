from django.db import models

# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField()
    ruc= models.IntegerField()

    def __str__(self):
        return self.name
