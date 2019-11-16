from django.core.management.base import BaseCommand, CommandError
import os
from os.path import normpath, basename
import sys
import xlrd
from candidature_master.models import Candidature
from collections import OrderedDict
from sow_master.models import SOW
from account_master.models import SPOC
from django.conf import settings

import pdb
reload(sys)
sys.setdefaultencoding('utf-8')



class Command(BaseCommand):
    help = 'update sow values'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('sowfile', nargs='+', type=str)

    def handle(self, *args, **options):

        
        file_path = os.path.join(settings.BASE_DIR, 'SOW Tracker_v0.1 Megha.xlsx')

        workbook = xlrd.open_workbook(file_path)
        sh = workbook.sheet_by_index(0)
        for rownum in range(0, sh.nrows):
            row_values = sh.row_values(rownum)
            sow_id= row_values[13]
            new_SPOC= row_values[15]
            new_client_group_head=row_values[17]
            new_line_manager=row_values[18]
            new_requestor=row_values[19]
            if sow_id :
               sow_objects=SOW.objects.all().filter(SOW_ID=sow_id)

               if sow_objects.count() > 0:
                    try:
                        for sow in sow_objects:
                            ressource_request=sow.resource_requests.all()
                            for req in ressource_request :
                                new_SPOC_obj,c = SPOC.objects.get_or_create(name=new_SPOC)
                                req.SPOC=new_SPOC_obj
                                req.client_group_head=new_client_group_head
                                req.requestor=new_requestor.replace(u'\xa0', u' ')
                                req.save()
                            sow.line_manager= new_line_manager
                            sow.last_moddified_by_id=1 
                            sow.save()
                    except Exception as e :
                        print e
                        print "sow_id",sow_id
                

                    
                   
        self.stdout.write(self.style.SUCCESS('Successfully Updated '))
    







# def saveToModel(path) :
#     workbook = xlrd.open_workbook(path)
#     sh = workbook.sheet_by_index(0)
    
#     exitCondidate=[]
    
#     for rownum in range(0, sh.nrows):
#         if rownum ==0 :
#             keys= sh.row_values(0)                    
#         else :
#             row_values = sh.row_values(rownum)
            
#             nameIndex=keys.index("Name")
#             skillIndex=keys.index("Skill")
#             levelIndex=keys.index("Interview Level")
#             queIndex=keys.index("Questions")
            
#             emp_name= row_values[nameIndex]
#             skill=row_values[skillIndex]
#             question=row_values[queIndex]
#             try:
#                 avaialble=Candidature.objects.get(resource__employee_name__contains=emp_name,
#                             resource__primary_skills__name__contains=skill
#                                        )
#                 print avaialble.candidatures.employee_name
#             except Candidature.DoesNotExist:
#                 queObj=QuestionText()
#                 queObj.emp_name=emp_name
#                 queObj.technology=skill
#                 queObj.text=question
#                 #queObj.save()
            
            


                    




        




        
        
        