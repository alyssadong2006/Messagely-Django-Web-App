"""
This represents all the forms
"""
from django import forms
#from . import models

class ExampleSignupForm(forms.Form):
    """
    This is the Example sign up form
    """
    first_name = forms.CharField(label = 'First Name', max_length = 50)
    last_name = forms.CharField(label = 'Last Name', max_length = 50)
    email = forms.EmailField()
    gender = forms.ChoiceField(
        label = 'Gender',
        required = False,
        choices = [
            (None, '-----'),
            ('m', 'Male'),
            ('f', 'Female'),
            ('n', 'Non-binary'),
        ]
    )
    receive_newsletter = forms.BooleanField(
        required = False,
        label = "Do you wish to receive our newsletter?"
    )
# class PhotoForms(forms.ModelForm):
#     class Meta:
#         model = models.Contact
#         fields = ['first_name', 'last_name', 'photo']
