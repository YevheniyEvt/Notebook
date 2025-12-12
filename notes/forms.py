from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button, Submit
from django import forms
from django.urls import reverse

from notes.models import Topic, Section, Code, Article, Links, Image


class BaseSectionTopicForm(forms.ModelForm):
    form_id = None
    class Meta:
        fields = ('title', 'description', 'bootstrap_icon_name')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.form_id
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


class TopicForm(BaseSectionTopicForm):
    form_id = 'hx-topic-form'

    class Meta(BaseSectionTopicForm.Meta):
        model = Topic


class SectionForm(BaseSectionTopicForm):
    form_id = 'hx-section-form'

    class Meta(BaseSectionTopicForm.Meta):
        model = Section


class SectionCodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-code-form'
        self.fields['content'].label = ''


class SectionArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-article-form'
        self.fields['content'].label = ''


class SectionLinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ('title', 'content', 'url',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-link-form'


class SectionImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'image_file',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-image-form'
        self.helper.attrs = {
            'hx-post':  reverse('notes:image_create', kwargs={'pk': section_id}),
            'hx-target': '#image-create',
        }

        self.helper.layout = Layout(
            'title',
            'description',
            'image_file',
            Submit(
                value='Add',
                name='Add',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get="#",
                hx_target="#image-create",
                hx_swap="delete",
                hx_trigger="click",
            )
        )

class SectionImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-image-form'
        self.helper.attrs = {
            'hx-post':  reverse('notes:image_update', kwargs={'pk': self.instance.id}),
            'hx-target': f'#image-{ self.instance.id }',
        }

        self.helper.layout = Layout(
            'title',
            'description',
            'image_file',
            Submit(
                value='Update',
                name='Update',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:image_list', kwargs={'pk': section_id}),
                hx_target = f"#image-{ self.instance.id  }",
                hx_select = f"#image-{ self.instance.id  }",
                hx_swap = "outerHTML",
            )
        )