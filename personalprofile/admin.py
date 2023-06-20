from django.contrib import admin
from . import models

class ProfileAdmin(admin.ModelAdmin):
    """Admin class for the Profile model"""
    list_display = ("user", "name", "phone_number", "date_of_birth")


class AddressAdmin(admin.ModelAdmin):
    """Admin class for the Address model"""
    list_display = ("address_1", "address_2", "city", "postcode", "profile", "current")

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Address, AddressAdmin)
