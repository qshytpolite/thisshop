from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, Div


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                             'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'px-4 py-3.5 bg-white text-gray-800 w-full text-sm border-b focus:border-gray-800 outline-none'}))

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(

                Column('first_name'),
                Column('last_name'),
                css_class='grid md:grid-cols-2 gap-4'
            ),
            Row(
                Column('address'),
                Column('email'),
                css_class='grid md:grid-cols-2 gap-4'
            ),
            Row(
                Column('phone_number'),
                Column('postal_code'),
                css_class='grid md:grid-cols-2 gap-4'
            ),
            Row(
                Column('city'),
                Column('country'),
                css_class='grid md:grid-cols-2 gap-4'
            ),

            Div(
                Submit('submit', 'Proceed to Payment',
                       css_class='w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700'),
                css_class='flex gap-4 max-md:flex-col mt-8'
            ),
        )
