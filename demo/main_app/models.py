from django.db import models

#to use the django's bultin authentication User need to import this
from django.contrib.auth.models import User



# Create your models here.

#the following model is for a normal user database
class Users(models.Model):
    first_name = models.CharField(max_length=32, null = False)
    last_name = models.CharField(max_length=32, null = False)
    email = models.EmailField(max_length=64, unique=True, null = False)
    url = models.URLField(max_length=128, null = True)
    # password

    def __str__(self):
        return self.first_name


#this model is to register user in the django's builtin Model User
#and make the one to one relationship with that models

class UserProfileInfo(models.Model):
    #HERE IS the main part
    #setting up this model with User model with one to one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #for some additional info specific for this models
    profile_pic = models.ImageField(upload_to='main_app/profile_pics', blank=True)
    #to working with picture we need a package
    # pip install pillow to use this!
    #if this command failed to execute then run the following
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    portfolio_site = models.URLField(blank=True)
    #blank means we can entry empty values in the databases


    #to return the name of this class we return the user name of this class
    def __str__(self):
        return self.user.username
