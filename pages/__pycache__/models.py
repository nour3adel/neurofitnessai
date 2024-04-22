from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator

class UserProfile(models.Model):
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
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Boolean flag and staff privileges
    is_admin = models.BooleanField(default=False)
    
    # Boolean flag fo Verification
    is_verified = models.BooleanField(default=False)

    # Date and time of user registration
    registration_date = models.DateTimeField(default=timezone.now)  # Use timezone.now without parentheses
    
     # Verification code as a 6-digit integer
    verification_code = models.CharField(max_length=6, default='', validators=[MaxLengthValidator(limit_value=6)])

    # Method of registration with choices
    registration_method = models.CharField(max_length=100, choices=METHOD_CHOICES, default='Default')

    def __str__(self):
        return self.username
      