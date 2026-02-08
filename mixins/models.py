from django.db import models


class LastVisitedMixin(models.Model):
    last_visited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True