from django.db import models

# Create your models here.
class Contact(models.Model):
    """Contact table"""
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class UploadedImage(models.Model):
    title = models.CharField(max_length=100) #Title for the image
    image = models.ImageField(upload_to='uploaded_images/') #save images to this


def _str_ (self):
        return self.title    