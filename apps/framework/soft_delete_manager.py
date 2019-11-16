from django.db import models


class SoftDeleteManager(models.Manager):
    ''' Use this manager to get objects that have a deleted field '''

    def all(self):
        return super(SoftDeleteManager,
                     self).all().filter(
            deleted=False)

    def all_with_deleted(self):
        return super(SoftDeleteManager, self).get_query_set()

    def deleted_set(self):
        return super(SoftDeleteManager,
                     self).get_query_set().filter(deleted=True)
