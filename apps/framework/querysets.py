from django.db import models


class BaseQueryset(models.QuerySet):

    def all(self):
        return self.exclude(deleted=True)
