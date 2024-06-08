from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'block text-sm font-medium text-gray-700'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'block text-sm font-medium text-gray-700'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'block text-sm font-medium text-gray-700'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'block text-sm font-medium text-gray-700'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'block text-sm font-medium text-gray-700'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'block text-sm font-medium text-gray-700'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'block text-sm font-medium text-gray-700'}))
