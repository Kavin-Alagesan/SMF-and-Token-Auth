from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class StudentDetailModel(models.Model):
    father_name=models.CharField(max_length=30, default=None,unique=True)
    occupation=models.CharField(max_length=30, default=None)
    address=models.CharField(max_length=100, default=None)
    
    def __str__(self):
        return self.father_name

class ProgressModel(models.Model):
    CHOICES_CLASS=[
        ("First Grade","First Grade"),
        ("Second Grade","Second Grade"),
        ("Third Grade","Third Grade"),
        ("Fourth Grade","Fourth Grade"),
        ("Fifth Grade","Fifth Grade"),
        ("Sixth Grade","Sixth Grade"),
        ("Seventh Grade","Seventh Grade"),
        ("Eighth Grade","Eighth Grade"),
    ]
    name=models.CharField(max_length=30, default=None)
    student_class=models.CharField(max_length=25,choices=CHOICES_CLASS, default=None)
    marks=models.IntegerField(default=None,validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    father_name=models.ForeignKey(StudentDetailModel,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.name



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
