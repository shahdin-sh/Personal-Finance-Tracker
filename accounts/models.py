from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        
        # django will Normalize the email address by lowercasing the domain part of it.
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    def create_staffuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False) 
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # Add related_name to resolve the conflict, because both User and CustomUser use the same related name 
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set',  # this is a unique reverse relation name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permissions_set',  # this is a unique reverse relation name
        blank=True
    )

    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username
    