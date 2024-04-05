import os
import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from api.manager import UserManager
# Create your models here.

Role=(
    ('Admin','Admin'),
    ('Gerant', 'Gerant'),
    ('Agent', 'Agent'),
)  
def image_uoload_profile_agent(instance,filname):
    imagename,extention =  filname.split(".")
    return "agent/%s.%s"%(instance.id,extention)

class UserAub(AbstractBaseUser,PermissionsMixin):
    nom = models.CharField(max_length=50,blank=True)
    prenom = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=16,unique=True)
    username = models.CharField(max_length=16,unique=True,null=True)
    email = models.EmailField(max_length=50,blank=True)
    address = models.CharField(max_length=200,)
    post = models.CharField(max_length=200,null=True)
    image=models.ImageField(upload_to=image_uoload_profile_agent ,null=True,blank=True) 
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    restricted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role= models.CharField(max_length=30, choices=Role,null=True,default='Gerant')
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    number_attempt= models.IntegerField(default=0)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    def __str__(self): 
        return self.username or "N/A"
    
class Direction(models.Model):
    nom = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100,null=True)

    def __str__(self): 
        return self.code     

class Archive(models.Model):
    nom = models.CharField(max_length=100, null=True)
    date_ajout = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom  

class Agent(UserAub):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, null=True) 
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, null=True) 

    def __str__(self): 
        return self.username 
        
#--------Girant -----------
class Gerant(UserAub):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, null=True) 
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, null=True) 
    def __str__(self): 
        return self.username 
    
#-------Admin------------- 
class Admin(UserAub):
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, null=True) 
    def __str__(self): 
        return self.phone or "N/A"    
    

    
def uoload_document(instance, filname):
    extention = os.path.splitext(filname)[1]
    unique_filename = f"{instance.id}{extention}"
    return os.path.join("gerant", unique_filename)  
 
def generate_unique_code():
    return str(uuid.uuid4().hex[:6].upper()) 
class Documents(models.Model):
    sujet = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100,null=True ,default=generate_unique_code,editable=False)
    description = models.TextField(max_length=400,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE,null=True)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, null=True)
    date_ajout = models.DateTimeField(auto_now=True,null=True)
    archives = models.ForeignKey(Archive, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.sujet 
    
def uoload_document_avis(instance, filname):
    extention = os.path.splitext(filname)[1]
    unique_filename = f"{instance.id}{extention}"
    return os.path.join("avis", unique_filename)   
    
class Avis(models.Model):
    titre = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=500,null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Assurez-vous que null=False
    user = models.ManyToManyField(UserAub, related_name='avis_users')
    date = models.DateTimeField(auto_now=True,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    def __str__(self):
            return self.titre 

class procedur(models.Model):
    titre = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=400,null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Assurez-vous que null=False
    user = models.ManyToManyField(UserAub, related_name='procedure_users')
    date = models.DateTimeField(auto_now=True,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    def __str__(self):
            return self.titre 
    
def generate_unique_note_code():
    return str(uuid.uuid4().hex[:6].upper())    
class note(models.Model):
    titre = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=400,null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Assurez-vous que null=False
    user = models.ManyToManyField(UserAub, related_name='notes_users')
    code = models.CharField(max_length=100,null=True ,default=generate_unique_note_code,editable=False)
    date = models.DateTimeField(auto_now=True,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    def __str__(self):
        return str(self.titre) if self.titre else "Titre par défaut"
    
def generate_unique_decision_code():
    return str(uuid.uuid4().hex[:6].upper())    
class decision(models.Model):
    titre = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=400,null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Assurez-vous que null=False
    user = models.ManyToManyField(UserAub, related_name='decision_users')
    code = models.CharField(max_length=100,null=True ,default=generate_unique_decision_code,editable=False)
    date = models.DateTimeField(auto_now=True,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    def __str__(self):
        return str(self.titre) if self.titre else "Titre par défaut"    

class charts(models.Model):
    titre = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=400,null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Assurez-vous que null=False
    user = models.ManyToManyField(UserAub, related_name='chartes_users')
    date = models.DateTimeField(auto_now=True,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    def __str__(self):
        return self.titre or "Titre par défaut"

class TextGouvernance(models.Model):
    titre = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=400,null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Assurez-vous que null=False
    user = models.ManyToManyField(UserAub, related_name='gouvernance_users')
    date = models.DateTimeField(auto_now=True,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    def __str__(self):
            return self.titre     
def generate_unique_plotique_code():
    return str(uuid.uuid4().hex[:6].upper()) 
class plotique(models.Model):
    titre = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=400,null=True)
    code = models.CharField(max_length=100,null=True ,default=generate_unique_plotique_code,editable=False)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  # Assurez-vous que null=False
    user = models.ManyToManyField(UserAub, related_name='plotique_users')
    date = models.DateTimeField(auto_now=True,null=True)
    file = models.FileField(upload_to =uoload_document,null=True)
    def __str__(self):
            return self.titre             
