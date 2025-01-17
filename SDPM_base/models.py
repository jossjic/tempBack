from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
class Item(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class AppUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=45, unique=True)
    user_first_name = models.CharField(max_length=45, blank=True, null=True)
    user_last_name = models.CharField(max_length=45, blank=True, null=True)
    user_role = models.IntegerField()
    user_picture = models.CharField(max_length=100, blank=True, null=True)
    user_norm_accepted = models.BooleanField(default=False)
    password = models.CharField(max_length=255)  # New password field

    class Meta:
        db_table = 'appuser'  # Nombre exacto de la tabla en la base de datos
        managed = False       # Desactiva la gestión de Django

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    # Indica que 'email' es el campo principal para el login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Campos obligatorios adicionales

    def __str__(self):
        return self.user_email

