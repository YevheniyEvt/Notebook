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


class TopicCreateForm(forms.ModelForm):
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
        self.helper.attrs = {
            'hx-post':  reverse('notes:topic_create'),
            'hx-target': f'#create-topic',
        }

        self.helper.layout = Layout(
            Div(
                'title',
                'bootstrap_icon_name',
                css_class='d-inline-flex gap-4'
            ),
            'description',
            Submit(
                value='Create',
                name='Create',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:topic_list'),
                hx_target = f"#create-topic",
                hx_select = f"#create-topic",
                hx_swap = "outerHTML",
            )
        )

class TopicUpdateForm(forms.ModelForm):
    class Meta(TopicCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-topic-form'
        self.helper.attrs = {
            'hx-post':  reverse('notes:topic_update', kwargs={'pk': self.instance.id}),
            'hx-target': f'#topic-{ self.instance.id }',
        }

        self.helper.layout = Layout(
            Div(
                'title',
                'bootstrap_icon_name',
                css_class='d-inline-flex gap-4'
            ),
            'description',
            Submit(
                value='Create',
                name='Create',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:topic_list'),
                hx_target = f"#topic-{ self.instance.id }",
                hx_select = f"#topic-{ self.instance.id }",
                hx_swap = "outerHTML",
            )
        )

class SectionCreateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('title', 'description', 'bootstrap_icon_name')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        topic_id = kwargs.pop('topic_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-form'
        self.helper.attrs = {
            'hx-post':  reverse('notes:section_create', kwargs={'pk': topic_id}),
            'hx-target': f'#create-section',
        }

        self.helper.layout = Layout(
            Div(
                'title',
                'bootstrap_icon_name',
                css_class='d-inline-flex gap-4'
            ),
            'description',
            Submit(
                value='Create',
                name='Create',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:topic_detail', kwargs={'pk': topic_id}),
                hx_target = f"#create-section",
                hx_select = f"#create-section",
                hx_swap = "outerHTML",
            )
        )

class SectionUpdateForm(forms.ModelForm):
    class Meta(SectionCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-form'
        self.helper.attrs = {
            'hx-post':  reverse('notes:section_update', kwargs={'pk': self.instance.id}),
            'hx-target': f'#section-{ self.instance.id}',
        }

        self.helper.layout = Layout(
            Div(
                'title',
                'bootstrap_icon_name',
                css_class='d-inline-flex gap-4'
            ),
            'description',
            Submit(
                value='Update',
                name='Update',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:topic_detail', kwargs={'pk': self.instance.topic_id}),
                hx_target = f"#section-{ self.instance.id}",
                hx_select = f"#section-{ self.instance.id}",
                hx_swap = "outerHTML",
            )
        )

class SectionCodeCreateForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        section_id= kwargs.pop('section_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-code-form'
        self.fields['content'].label = ''
        self.helper.attrs = {
            'hx-post':  reverse('notes:code_create', kwargs={'pk': section_id}),
            'hx-target': f'#code-create',
        }
        self.helper.layout = Layout(
            'content',
            Submit(
                value='Create',
                name='Create',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get="#",
                hx_target="#code-create",
                hx_swap="delete",
                hx_trigger="click",
            )
        )

class SectionCodeUpdateForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-code-form'
        self.fields['content'].label = ''
        self.helper.attrs = {
            'hx-post':  reverse('notes:code_update', kwargs={'pk': self.instance.id}),
            'hx-target': f'#code-{ self.instance.id  }',
        }
        self.helper.layout = Layout(
            'content',
            Submit(
                value='Update',
                name='Update',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:code_list', kwargs={'pk': self.instance.section_id}),
                hx_target = f"#code-{ self.instance.id}",
                hx_select = f"#code-{ self.instance.id}",
                hx_swap = "outerHTML",
            )
        )


class SectionArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-article-form'
        self.fields['content'].label = ''
        self.helper.attrs = {
            'hx-post':  reverse('notes:article_create', kwargs={'pk': section_id}),
            'hx-target': f'#article-create',
        }
        self.helper.layout = Layout(
            'content',
            Submit(
                value='Create',
                name='Create',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get="#",
                hx_target="#article-create",
                hx_swap="delete",
                hx_trigger="click",
            )
        )


class SectionArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-article-form'
        self.fields['content'].label = ''
        self.helper.attrs = {
            'hx-post':  reverse('notes:article_update', kwargs={'pk': self.instance.id}),
            'hx-target': f'#article-{ self.instance.id  }',
        }
        self.helper.layout = Layout(
            'content',
            Submit(
                value='Update',
                name='Update',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:article_list', kwargs={'pk': self.instance.section_id}),
                hx_target = f"#article-{ self.instance.id}",
                hx_select = f"#article-{ self.instance.id}",
                hx_swap = "outerHTML",
            )
        )


class SectionLinksCreateForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ('title', 'content', 'url',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'hx-section-link-form'
        self.fields['content'].label = ''
        self.helper.attrs = {
            'hx-post':  reverse('notes:link_create', kwargs={'pk': section_id}),
            'hx-target': f'#link-create',
        }
        self.helper.layout = Layout(
            'title',
            'content',
            'url',
            Submit(
                value='Create',
                name='Create',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get="#",
                hx_target="#link-create",
                hx_swap="delete",
                hx_trigger="click",
            )
        )

class SectionLinksUpdateForm(forms.ModelForm):
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
        self.fields['content'].label = ''
        self.helper.attrs = {
            'hx-post':  reverse('notes:link_update', kwargs={'pk': self.instance.id}),
            'hx-target': f'#link-{ self.instance.id  }',
        }
        self.helper.layout = Layout(
            'title',
            'content',
            'url',
            Submit(
                value='Update',
                name='Update',
                css_class='btn btn-primary btn-sm',
            ),
            Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = reverse('notes:link_list', kwargs={'pk': self.instance.section_id}),
                hx_target = f"#link-{ self.instance.id}",
                hx_select = f"#link-{ self.instance.id}",
                hx_swap = "outerHTML",
            )
        )


class SectionImageCreateForm(forms.ModelForm):
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