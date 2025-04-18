from django import forms

from client.models import Client, Message, Mail


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['owner']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment (optional)',
                'rows': 4
            }),
            'owner': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['owner']
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the topic of the message'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here...',
                'rows': 6
            }),
            'owner': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        exclude = ['status', 'is_active', 'owner']

        widgets = {
            'time_for_sending': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'recipients': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['recipients'].queryset = Client.objects.filter(owner=self.user)
            self.fields['message'].queryset = Message.objects.filter(owner=self.user)


class MailManagerForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['is_active']
