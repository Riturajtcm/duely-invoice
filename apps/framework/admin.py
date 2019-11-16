from django.contrib import admin
from django.conf import settings
from .models import *
import logging

# Get an instance of a logger
logger = logging.getLogger("account_invoicing")


class BaseAdmin(admin.ModelAdmin):

    """docstring for CustomerAdmin"""
    list_per_page = 10
    exclude = ['created_on', 'created_by',
               'last_moddified_on', 'last_moddified_by', 'version']
    save_on_top = True
    view_on_site = False
    # def has_change_permission(self, request,obj=obj):
    #     return settings.DEFAULT_ADMIN_DELETE_BEHAVIOUR

    # def has_delete_permission(self, request):
    #     return settings.DEFAULT_ADMIN_DELETE_BEHAVIOUR

    # def has_add_permission(self, request):
    #     return settings.DEFAULT_ADMIN_ADD_BEHAVIOUR

    def has_module_permission(self, request):
        return True

    # def save_model(self, request, obj, form, change):
    #     import logging
    #     db_logger = logging.getLogger('db')

    #     db_logger.info('info message')
    #     db_logger.warning('warning message')

    #     try:
    #         1/0
    #     except Exception as e:
    #         db_logger.exception(e)
    #     obj.created_by = request.user

    #     super(BaseAdmin).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.user = request.user
        super().delete_model(request, obj)
