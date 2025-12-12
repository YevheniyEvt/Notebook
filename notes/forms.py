from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms

from notes.models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'description', 'bootstrap_icon_name')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-topic-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.layout = Layout(
            Div(
                'title',
                'bootstrap_icon_name',
                css_class='d-inline-flex gap-4'
            ),
            'description',
        )