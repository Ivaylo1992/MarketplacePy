from django import forms

from MarketplacePy.conversations.models import Message


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here...',
            }),
        }
