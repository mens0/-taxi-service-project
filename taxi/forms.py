from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )


class CarCreateForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class LicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(required=True)

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        data = self.cleaned_data.get("license_number")

        if not data[:3].isupper():
            raise forms.ValidationError("First 3 letters should be uppercase")
        elif not data[5:].isdigit():
            raise forms.ValidationError("Last 5 letters should be numbers")
        elif len(data) != 8:
            raise forms.ValidationError("Password should be 8 symbols long")

        return data


class DriverSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by model"})
    )


class ManufacturerSearchForm(forms.Form):
    manufacturer = forms.CharField(
        max_length=255,
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by manufacturer"}, ))
