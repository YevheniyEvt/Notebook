from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button, Submit
from django import forms
from django.urls import reverse

from notes.models import Topic, Section, Code, Article, Links, Image


class BaseNoteHTMXForm(forms.ModelForm):
    """
      Base HTMX-aware ModelForm for Note-like models that supports both Create and Update workflows.

      This form encapsulates common behavior shared by all note-related forms:
      - Automatically detects whether the form is used for creation or update.
      - Builds HTMX attributes (`hx-post`, `hx-target`, etc.) dynamically
        according to the current operation.
      - Integrates with django-crispy-forms via FormHelper.
      - Provides reusable action and cancel buttons with HTMX-powered behavior.

      Expected conventions:
      - The associated model MUST implement:
          - `get_create_url(...)` (class method or static method)
          - `get_update_url(...)` (instance method)
          - `get_hx_rerender_url(...)` (class method or static method)

      Extension points:
      - `fields_layout` can be overridden to customize field ordering or layout.
      - `action_button` can be overridden to change submit button behavior or style.
      - `cancel_form_button` can be overridden to customize cancel action logic.

      HTMX behavior:
      - On submit, the form is posted via `hx-post` to the resolved action URL.
      - On cancel, the form is replaced (`outerHTML`) with a re-rendered fragment.

      This class is intended to be subclassed and should not be used directly
      without following the required naming and model conventions.
      """

    def __init__(self, *args, **kwargs):
        self.related_instance_id = kwargs.pop('related_instance_id', None)
        super().__init__(*args, **kwargs)

        self.is_create_form = self.instance.id is None
        self.is_update_form = self.instance.id is not None

        self.hx_target = (
            f'#create-{self._meta.model.__name__.lower()}'
            if self.is_create_form
            else f'#{self._meta.model.__name__.lower()}-{self.instance.id}'
    )
        self.form_action_url = (
                self._meta.model.get_create_url(related_instance_id=self.related_instance_id)
                if self.is_create_form
                else self.instance.get_update_url()
            )

        self.helper = FormHelper()
        self.helper.form_id = f'hx-create-{self._meta.model.__name__.lower()}'
        self.helper.attrs = {
            'hx-post': self.form_action_url,
            'hx-target': self.hx_target,
        }
        self.helper.layout = Layout(
            *self.fields_layout,
            self.action_button,
            self.cancel_form_button,
        )

    @property
    def fields_layout(self):
        return self.fields

    @property
    def action_button(self):
        return Submit(
                value='Create' if self.is_create_form else 'Update',
                name='Create' if self.is_create_form else 'Update',
                css_class='btn btn-primary btn-sm',
            )

    @property
    def cancel_form_button(self):
        return Button(
                value='Cancel',
                name='Cancel',
                css_class='btn btn-secondary btn-sm',
                hx_get = self._meta.model.get_hx_rerender_url(related_instance_id=self.related_instance_id),
                hx_target = self.hx_target,
                hx_select = self.hx_target,
                hx_swap = "outerHTML",
            )


class BaseTopicSectionHTMXForm(BaseNoteHTMXForm):
    fields_layout = [
        Div(
        'title',
        'bootstrap_icon_name',
        css_class='d-inline-flex gap-4'
        ),
        'description'
    ]

    class Meta:
        fields = ('title', 'description', 'bootstrap_icon_name')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

class TopicCreateHTMXForm(BaseTopicSectionHTMXForm):
    class Meta(BaseTopicSectionHTMXForm.Meta):
        model = Topic

class TopicUpdateHTMXForm(BaseTopicSectionHTMXForm):
    class Meta(BaseTopicSectionHTMXForm.Meta):
        model = Topic

class SectionCreateHTMXForm(BaseTopicSectionHTMXForm):
    class Meta(BaseTopicSectionHTMXForm.Meta):
        model = Section

class SectionUpdateHTMXForm(BaseTopicSectionHTMXForm):
    class Meta(BaseTopicSectionHTMXForm.Meta):
        model = Section


class SectionCodeCreateHTMXForm(BaseNoteHTMXForm):
    class Meta:
        model = Code
        fields = ('content',)

class SectionCodeUpdateHTMXForm(SectionCodeCreateHTMXForm):
    class Meta(SectionCodeCreateHTMXForm.Meta):
        pass


class SectionArticleCreateHTMXForm(BaseNoteHTMXForm):
    class Meta:
        model = Article
        fields = ('content',)

class SectionArticleUpdateHTMXForm(SectionArticleCreateHTMXForm):
    class Meta(SectionArticleCreateHTMXForm.Meta):
        pass


class SectionLinksCreateHTMXForm(BaseNoteHTMXForm):
    class Meta:
        model = Links
        fields = ('title', 'content', 'url',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1}),
        }

class SectionLinksUpdateHTMXForm(SectionLinksCreateHTMXForm):
    class Meta(SectionLinksCreateHTMXForm.Meta):
        pass


class SectionImageCreateHTMXForm(BaseNoteHTMXForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'image_file',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

class SectionImageUpdateHTMXForm(SectionImageCreateHTMXForm):
    class Meta(SectionImageCreateHTMXForm.Meta):
        fields = ('title', 'description',)