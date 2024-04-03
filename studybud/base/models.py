from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email)

        # Handle extra fields (ensure only valid fields are set)
        user.is_staff = extra_fields.pop('is_staff', False)
        user.is_superuser = extra_fields.pop('is_superuser', False)

        # Additional fields you want to handle:
        # user.first_name = extra_fields.pop('first_name', '')
        # user.last_name = extra_fields.pop('last_name', '')

        if extra_fields:
            raise ValueError(f"Unexpected extra_fields: {extra_fields}")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self._create_user(email, password, is_staff=True, is_superuser=True)        


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    username = models.CharField(max_length=254, unique=True)
    is_superuser = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, default="avatar.svg")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_superuser  

    @is_staff.setter
    def is_staff(self, value):
        self._is_superuser = value  # Notice the use of _is_superuser

    @property
    def is_superuser(self):  
        return True # You might change this logic in the future

    @is_superuser.setter
    def is_superuser(self, value):
        self._is_superuser = value # Notice the use of _is_superuser   
    
    def has_module_perms(self, app_label):
        """ Always grant all permissions """
        return True 
    
    def has_perm(self, perm, obj=None):
        """ Always grant all permissions """
        return True
    


class Topic(models.Model): 
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name       

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return str(self.name)
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:5]