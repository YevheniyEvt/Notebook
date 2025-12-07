from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Layout
from django import forms
from django.urls import reverse

from daybook.models import Entries


class EntriesCreateForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        required=True,
    )
    class Meta:
        model = Entries
        fields = ('text',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-entries-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('daybook:entries_create')


class EntriesUpdateForm(EntriesCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_url = reverse('daybook:entries_update', kwargs={'pk':self.instance.pk})
        self.helper.form_action = update_url
        self.helper.layout = Layout(
            'text',
            Button(
                value='Submit',
                name='Submit',
                css_class='btn btn-primary',
                hx_select='#hx-entries-form',
                hx_post=update_url,
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary',
                hx_get=reverse('daybook:entries_detail', kwargs={'pk': self.instance.pk}),
                hx_target=f'#entry-article-{self.instance.pk}',
                hx_swap='outerHTML',
            ),
        )