from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import models
from . import forms

@login_required
def create_profile(request):
    """Create a user profile.

    This view handles the creation of a user profile. If the user already has a
    profile, they are redirected to the view profile page.

    - GET request: Renders the create profile form.
    - POST request: Validates and processes the submitted form data.

    To create a profile the view expects the following form fields:
    - name
    - phone_number
    - date_of_birth
    - address_1
    - address_2
    - city
    - postcode
    """
    try:
        models.Profile.objects.get(user=request.user)
        messages.warning(request, "You have already created a profile - here it is!")
        return redirect("view_profile")
    except models.Profile.DoesNotExist:
        pass

    if request.method == "POST":
        profile_form = forms.ProfileForm(request.POST)
        address_form = forms.AddressForm(request.POST)

        if profile_form.is_valid() and address_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            address = address_form.save(commit=False)
            address.profile = profile
            address.current = True
            address.save()
            return redirect("view_profile")
    else:
        profile_form = forms.ProfileForm()
        address_form = forms.AddressForm()
    context = {
        "profile_form": profile_form,
        "address_form": address_form
    }
    return render(request, "create_profile.html", context)

@login_required
def view_profile(request):
    """View a user profile.

    This view enables a user to view their profile. If the user doesn't have a
    profile, they are redirected to the create profile page.

    - GET request: Renders the view profile form.
    """
    try:
        profile = models.Profile.objects.get(user=request.user)
    except models.Profile.DoesNotExist:
        messages.warning(request, "You don't have a profile yet. Please create one.")
        return redirect("create_profile")
    current_address = models.Address.objects.get(profile=profile, current=True)
    past_addresses = list(models.Address.objects.filter(profile=profile, current=False))
    context = {
        "profile": profile,
        "current_address": current_address,
        "past_addresses": past_addresses
    }
    return render(request, "view_profile.html", context)

@login_required
def update_profile(request):
    """Update a user profile.

    This view handles updating a user profile. If the user doesn't have a
    profile, they are redirected to the create profile page.

    - GET request: Renders the update profile form.
    - POST request: Validates and processes the submitted form data.

    To update a profile the view expects the following form fields:
    - name
    - phone_number
    - date_of_birth
    - address_1
    - address_2
    - city
    - postcode
    """
    try:
        profile = models.Profile.objects.get(user=request.user)
    except models.Profile.DoesNotExist:
        messages.warning(request, "You don't have a profile yet. Please create one.")
        return redirect("create_profile")

    current_address = models.Address.objects.get(profile=profile, current=True)

    if request.method == "POST":
        profile_form = forms.ProfileForm(request.POST, instance=profile)
        address_form = forms.AddressForm(request.POST)
        if profile_form.is_valid() and address_form.is_valid():
            new_address_data = address_form.cleaned_data
            if new_address_data["postcode"] != current_address.postcode:
                new_address = address_form.save(commit=False)
                new_address.profile = profile
                new_address.current = True
                new_address.save()

                current_address.current = False
                current_address.save()
            else:
                current_address.address_1 = new_address_data["address_1"]
                current_address.address_2 = new_address_data["address_2"]
                current_address.city = new_address_data["city"]
                current_address.save()

            profile_form.save(commit=False)
            profile_form.user = request.user
            profile_form.save()
            return redirect("view_profile")

    else:
        profile_form = forms.ProfileForm(instance=profile)
        address_form = forms.AddressForm(instance=current_address)
    context = {
        "profile_form": profile_form,
        "address_form": address_form
    }
    return render(request, "update_profile.html", context)

@login_required
def delete_profile(request):
    """Delete a user profile.

    This view handles the deletion of a user profile. Once the profile is
    deleted, the user is redirected to the home page.
    """
    profile = models.Profile.objects.get(user=request.user)
    profile.delete()
    return redirect("home")
