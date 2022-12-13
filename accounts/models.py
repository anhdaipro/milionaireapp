from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
GENDER_CHOICE=(
        ('1','MALE'),
        ('2','FEMALE'),
        ('3','ORTHER')
    )
AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20,null=True)
    name=models.CharField(max_length=40,null=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    social_id=models.CharField(max_length=2000,null=True)
    coins=models.FloatField(default=0)
    def __str__(self):
        return self.username

class Verifylink(models.Model):
    otp=models.CharField(max_length=10)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Verifyemail(models.Model):
    otp=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)