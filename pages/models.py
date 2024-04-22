from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#region[Pink] CustomUserManager  

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)
    
#endregion

#region[Violet] User 

class User(AbstractBaseUser):
    
    # Choices for user levels
    LEVEL_CHOICES = [
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ]

        # Choices for registration methods
    METHOD_CHOICES = [
            ('Default', 'Default'),
            ('Google', 'Google'),
            ('Facebook', 'Facebook'),
        ]
    
    # Basic user information
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128) 
    
    # User skill level with choices
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES, default='Beginner')

    # Email field with uniqueness constraint
    email = models.EmailField(unique=True)

    # User profile picture
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/logo2.png')

    # Boolean flag and staff privileges
    is_admin = models.BooleanField(default=False)
    

    # Boolean flag and staff privileges
    is_staff = models.BooleanField(default=False)
    
    # Boolean flag fo Verification
    is_verified = models.BooleanField(default=False)

    # Date and time of user registration
    registration_date = models.DateTimeField(default=timezone.now)  # Use timezone.now without parentheses
    
     # Verification code as a 6-digit integer
    verification_code = models.CharField(max_length=6, default='', validators=[MaxLengthValidator(limit_value=6)])

    # Method of registration with choices
    registration_method = models.CharField(max_length=100, choices=METHOD_CHOICES, default='Default')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Required for AbstractBaseUser
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
   
   #endregion