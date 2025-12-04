import django_tables2 as tables

from notebook.tasks.models import Task


class TaskTable(tables.Table):
    description = tables.TemplateColumn(orderable=False, verbose_name="Description", template_name="tasks/table/description_task_field.html")
    start_date = tables.Column(attrs={'td':{"style": "vertical-align: middle;", 'class': 'text-nowrap'}})
    end_date = tables.Column(attrs={'td': {"style": "vertical-align: middle;", 'class': 'text-nowrap'}})
    action = tables.TemplateColumn(orderable=False, verbose_name="", template_name="tasks/table/action_field.html", attrs={'td': {"style": "vertical-align: middle;"}})

    class Meta:
        model = Task
        template_name = "django_tables2/bootstrap.html"
        fields = ('description', 'start_date', 'end_date', 'action')
        attrs = {
            "class": "table table-hover mt-4",
        }
        row_attrs = {"class": lambda record: (
            "table-secondary" if record.is_canceled
            else "table-success" if record.is_completed
            else ""
        )}

        empty_text = 'No tasks'
