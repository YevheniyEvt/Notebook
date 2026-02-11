from crispy_forms.helper import FormHelper
from django import forms
from django.urls import reverse

from agent.models import Message

class MessageCreateForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


    def __init__(self, *args, **kwargs):
        self.chat_id = kwargs.pop('related_instance_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-message-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('chatbot:messages_create', kwargs={'pk': self.chat_id })



class WsMessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }