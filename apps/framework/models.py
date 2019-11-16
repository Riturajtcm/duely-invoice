from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .soft_delete_manager import SoftDeleteManager
# from CurrentUserMiddleWare import *





class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True,related_name='%(class)s_created',on_delete=models.PROTECT)
    last_moddified_on = models.DateTimeField(null=True, blank=True)
    last_moddified_by = models.ForeignKey(
        User, null=True, blank=True, related_name='%(class)s_modified',on_delete=models.PROTECT)
    version = models.CharField(max_length=10, default='0')
    deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()

    def save(self,*args, **kwargs):
        try:
            req = get_username().user
            if self.id:
                self.last_moddified_on = timezone.now()
                self.last_moddified_by = req
            else:
                self.created_by = req
        except:
            pass
        super(BaseModel, self).save()

    def delete(self):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True
