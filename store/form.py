from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'block w-full text-sm font-medium text-gray-700'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'block w-full text-sm font-medium text-gray-700'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'block w-full text-sm font-medium text-gray-700'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'block w-full text-sm font-medium text-gray-700'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'block w-full text-sm font-medium text-gray-700'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'block w-full text-sm font-medium text-gray-700'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'block w-full text-sm font-medium text-gray-700'}))

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('address'),
            Field('email'),
            Field('phone_number'),
            Field('postal_code'),
            Field('country'),
            Submit('submit', 'Proceed to Payment', css_class='w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700')
        )
