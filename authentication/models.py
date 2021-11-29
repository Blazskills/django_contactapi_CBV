from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

# What is the benefit of creating special or CustomUserManager





# class CustomUserManager(BaseUserManager):
#     def _create_user(self, email,password,first_name, last_name,mobile, **extra_fields):
#         if not email:
#             raise ValueError("Email must be provided")
#         if not password:
#             raise ValueError("Password is not provided")


#         user = self.model(
#             email = self.normalize_email(email),
#             first_name=first_name,
#             last_name = last_name,
#             mobile = mobile,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
                                        
#     def create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
#         extra_fields.setdefault('is_staff',True)
#         extra_fields.setdefault('is_active',True)
#         extra_fields.setdefault('is_superuser',False)
#         return self._create_user(email, password, first_name, last_name, mobile, password, **extra_fields)

#     def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
#         extra_fields.setdefault('is_staff',True)
#         extra_fields.setdefault('is_active',True)
#         extra_fields.setdefault('is_superuser',True)
#         return self._create_user(email, password, first_name, last_name, mobile, **extra_fields) 
 
 
 
 
class CustomUserMnanager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email should be provided"))
        email = self.normalize_email(email)
        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save()
        return new_user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser should have is_staff as True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser should have is_super as True"))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_("Superuser should have is_active as True"))

        return self.create_user(email, password, **extra_fields)   
        

# class User(AbstractBaseUser, PermissionsMixin):
class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    username = models.CharField(
        max_length=200, blank=False, null=True, default=None, db_index=True)
    email = models.EmailField(unique=True, null=False)
    mobile = models.CharField(max_length=50)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    bio = models.TextField(null=True)
    address = models.CharField(max_length=250)
    social_handle = models.CharField(max_length=200, null=True)
    Otp_Validation = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # avatar = CloudinaryField('image', null= True, default="avatar.svg")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = CustomUserMnanager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
