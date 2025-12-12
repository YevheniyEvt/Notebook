from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms

from notes.models import Topic, Section, Code, Article


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