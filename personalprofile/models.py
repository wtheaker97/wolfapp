import datetime as dt
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    """Abstract model to add timestamp each model instance
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False, help_text="Created at")
    modified_at = models.DateTimeField(auto_now=True, editable=True, null=True, blank=True, help_text="Modified at")

    class Meta:
        abstract = True


class Profile(BaseModel):
    """Model class to store Personal Profile data

    Inherits from the BaseModel class.
    Has a foreign key relationship to the User model to link each profile to a
    user.
    """

    def validate_date_of_birth(value):
        """Validator to ensure valid date of birth"""
        if value >= dt.date.today():
            raise ValidationError('Date of birth must be in the past.')

    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=100) # Put some restrictions on this - regex
    date_of_birth = models.DateField(validators=[validate_date_of_birth])

    @property
    def age(self):
        """Property to store the Profile's age"""
        today = dt.date.today()
        age = (today.year - self.date_of_birth.year -
            ((today.month <= self.date_of_birth.month) and
            (today.day < self.date_of_birth.day))
        )
        return age


class Address(BaseModel):
    """Model class to store Personal Address data

    Inherits from the BaseModel class.
    Has a foreign key relationship to the Profile model to link each address to
    a profile.
    """
    address_1 = models.CharField("Street Address 1", max_length=255, null=False, help_text="Address line 1")
    address_2 = models.CharField("Street Address 2", max_length=255, null=True, blank=True, help_text="Address line 2")
    city = models.CharField(max_length=64, null=False, help_text="City")
    postcode = models.CharField("Postcode", max_length=16, null=False, help_text="Postcode")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    current = models.BooleanField("Current Address", default=True)
