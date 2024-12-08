from django import forms


class TransactionForm(forms.Form):
    profile_id = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),  # Hidden field, as it is likely constant for CyberSource
    )
    access_key = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),  # Hidden field for CyberSource credentials
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=19.95,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
    )
    transaction_uuid = forms.CharField(
        max_length=32,
        widget=forms.HiddenInput(),
    )
    bill_to_forename = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    bill_to_surname = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    bill_to_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    locale = forms.ChoiceField(
        choices=[('en-us', 'English (US)'), ('en-gb', 'English (UK)')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    currency = forms.ChoiceField(
        choices=[('bwp', 'Botswana Pula'), ('usd', 'US Dollar')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    transaction_type = forms.ChoiceField(
        choices=[('sale', 'Sale'), ('authorization', 'Authorization')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    reference_number = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
    )
