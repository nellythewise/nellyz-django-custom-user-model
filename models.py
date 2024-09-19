from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    def create_user(self, first_name, middle_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address set.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, middle_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        user = self.create_user(
            first_name,
            middle_name,
            last_name,
            email,
            password,
            **extra_fields
        )
        user.save(using=self.db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'middle_name', 'last_name']

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)

