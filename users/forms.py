from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserBanForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)


class UserProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        label='New Password',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'})
    )

    class Meta:
        model = User
        fields = ['email', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user
