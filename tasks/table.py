import django_tables2 as tables

from tasks.models import Task


class TaskTable(tables.Table):
    description = tables.TemplateColumn(orderable=False, verbose_name="", template_name="tasks/table/description_task_field.html")
    start_date = tables.Column(attrs={'td':{"style": "vertical-align: middle;", 'class': 'text-nowrap'}}, verbose_name="Start")
    end_date = tables.Column(attrs={'td': {"style": "vertical-align: middle;", 'class': 'text-nowrap'}}, verbose_name="Deadline")
    action = tables.TemplateColumn(orderable=False, verbose_name="", template_name="tasks/table/action_field.html", attrs={'td': {"style": "vertical-align: middle;"}})

    # add id to div that wraps table
    table_container_id = "tasks-table"

    class Meta:
        model = Task
        fields = ('description', 'start_date', 'end_date', 'action')
        attrs = {
            "class": "table table-light mt-4",
        }
        row_attrs = {"class": lambda record: (
            "table-secondary" if record.is_canceled
            else "table-success" if record.is_completed
            else "table-light"
        )}

        empty_text = 'No tasks'
