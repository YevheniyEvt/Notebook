from crispy_forms.helper import FormHelper
from django import forms

from daybook.models import Entries


class EntriesForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        required=True,
    )
    class Meta:
        model = Entries
        fields = ('title', 'text')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-entries-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'