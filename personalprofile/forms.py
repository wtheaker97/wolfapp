from django import forms
from . import models

class ProfileForm(forms.ModelForm):
    """A form for creating or updating a user profile.

    Usage:
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()

    Note: the user field is not included in the form so must be added separately
    before saving the instance (see above example)
    """
    class Meta:
        model = models.Profile
        fields = ["name", "phone_number", "date_of_birth"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }


class AddressForm(forms.ModelForm):
    """A form for creating or updating a profile address.

    Usage:
    form = AddressForm(request.POST)
    if form.is_valid():
        address = form.save(commit=False)
        address.profile = profile
        address.current = True
        address.save()

    Note: the profile and current fields are not included in the form so must be
    added separately before saving the instance (see above example). If creating
    a new address the current field of the old address should be marked False.
    """
    class Meta:
        model = models.Address
        fields = ["address_1", "address_2", "city", "postcode"]
