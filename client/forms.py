from django import forms

from client.models import Client, Message, Mail


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


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
