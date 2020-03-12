from django.db import models
from django.contrib.auth.models import AbstractBaseUser #Django default user
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings #get settings.py file from project settings

# Create your models here.
class UserProfileManager(BaseUserManager):
    """ MANAGER FOR USER PROFILE """
    def create_user(self, email, name, password = None):
        """CREATE A NEW USER PROFILE"""
        if not email: 
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email = email, name = name)
        
        user.set_password(password) #encrypts the password
        user.save(using=self._db) #standard procedure for saving objects in django
        return user

    def create_superuser(self, email, name, password):
        """ CREATE AND SAVE NEW SUPERUSER WITH GIVEN DETAILS"""
        user = self.create_user(email, name, password)

        user.is_superuser = True #provided by Permissions Mixin
        user.is_staff = True
        user.save(using=self._db)
        return user


#CREATING USER PROFILE MODEL
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """DB model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' #replace default user name with email
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """RETRIEVE FULL NAME OF USER"""
        return self.name
    
    def get_short_name(self):
        """RETRIEVE SHORT NAME OF USER"""
        return self.name
    
    def __str__(self):
        """RETURN STRING REPRESENTATION OF OUR USER MODEL"""
        return self.email #recommended for all django models 
    

class ProfileFeedItem(models.Model):
    """PROFILE STATUS UPDATE"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE #when remote field is deleted then delete this item also
    )
    status_text = models.CharField(max_length=255)#text of the feed update
    created_on = models.DateTimeField(auto_now_add=True) #automatically add date time stamp once item created

    def __str__(self):
        """Return model as string"""
        return self.status_text
