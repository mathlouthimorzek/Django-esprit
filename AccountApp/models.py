from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Add any additional fields you want for your custom user model
    pass

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True , validators=[MinLengthValidator(6)])
    phone = models.CharField(max_length=8)
    specialties = models.ManyToManyField(Specialty, related_name='doctors') 
    class Meta:
       verbose_name = 'Doctor'
       verbose_name_plural = 'Doctors'

phone_validator = RegexValidator(
    regex=r"^\d{8}$",
    message="Le téléphone doit contenir 8 chiffres."
   
)
def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("Date invalide")
class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[RegexValidator(r'^\d{8}$', message='Le numéro de CIN doit contenir exactement 8 chiffres.')])
    phone = models.CharField(
        max_length=8, validators=[phone_validator]
    )
    birth_date = models.DateField(validators=[validate_past_date])

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'








