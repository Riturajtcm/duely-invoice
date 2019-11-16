from django.db import models


class BaseManager(models.Manager):

    def get_queryset(self):
        # Important!
        return self.queryset(self.model, using=self._db).exclude(deleted=True)

    def all(self):
        return self.exclude(deleted=True)
