import os
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from api.manager import UserManager
# Create your models here.

Role=(
    ('Girant', 'Girant'),
    ('Agent', 'Agent'),
)  

class UserAub(AbstractBaseUser,PermissionsMixin):
    nom = models.CharField(max_length=50,blank=True)
    prenom = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=16,unique=True)
    email = models.EmailField(max_length=50,blank=True)
    address = models.CharField(max_length=200,)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    restricted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role= models.CharField(max_length=30, choices=Role, default='Girant')
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    number_attempt= models.IntegerField(default=0)
    objects = UserManager()

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []

    def __str__(self): 
        return self.nom 
    
class Direction(models.Model):
    nom = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100,null=True)

    def __str__(self): 
        return self.nom     

def image_uoload_profile_agent(instance,filname):
    imagename,extention =  filname.split(".")
    return "agent/%s.%s"%(instance.id,extention)    

class Agent(UserAub):
    image=models.ImageField(upload_to=image_uoload_profile_agent ,null=True)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, null=True)    
    def __str__(self): 
        return self.phone 
        
#--------Girant -----------
def image_uoload_profile_girant(instance,filname):
    imagename,extention =  filname.split(".")
    return "girant/%s.%s"%(instance.id,extention)

class Girant(UserAub):
    image=models.ImageField(upload_to=image_uoload_profile_girant ,null=True) 
    def __str__(self): 
        return self.phone 
    
# def uoload_document(instance,filname):
#     imagename,extention =  filname.split(".")
#     return "document/%s.%s"%(instance.id,extention)
def uoload_document(instance, filname):
    extention = os.path.splitext(filname)[1]
    unique_filename = f"{instance.id}{extention}"
    return os.path.join("girant", unique_filename)   
 
class Documents(models.Model):
    sujet = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100,null=True)
    description = models.TextField(max_length=400,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    def __str__(self):
        return self.sujet    
    
