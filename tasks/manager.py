from datetime import date

from django.db import models

class TaskManager(models.Manager):

    def terminated_tasks(self):
        return self.filter(end_date__lt=date.today(), status=self.model.Status.IN_PROGRESS)

    def tasks_with_today_deadline(self):
        return self.filter(end_date=date.today(), status=self.model.Status.IN_PROGRESS)