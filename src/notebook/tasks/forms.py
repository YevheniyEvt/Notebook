from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'), initial=date.today)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'), initial=date.today)

    class Meta:
        model = Task
        fields = ( 'start_date', 'end_date', 'title', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-create-task-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.layout = Layout(
            Div(
                'start_date',
                'end_date',
                css_class='d-inline-flex gap-4'
            ),
            'title',
            'description',
        )