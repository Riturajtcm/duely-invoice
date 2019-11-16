from django.core.management.base import BaseCommand
from account_master.models import *
from location_master.models import *
from skill_master.models import *
from demand_master.models import *
from candidature_master.models import *
from framework.utils import *
import copy


class Command(BaseCommand):
    help = 'Exports All customers Data'
    db_name = 'pmo_reports'
    table_name = 'onboarding_reports'
    export_to_excel = True
    columns = ['Sr No',
               'Employee ID',
               'Employee Name',
               'Resource Status',
               'Summary Status',
               'Employee Type',
               'Location',
               'Selection Date',
               'Department',
               'Sub Department',
               'Tech/Skill',
               'RR Code',
               'JC Code',
               'SOW',
               'Synechron POC',
               'Synechron Contact',
               'Client Group Head',
               'HSBC Hiring Manager',
               'Requestor',
               'Exp in Months',
               'Project Role (SOW)',
               'SOW Start Date',
               'SOW End Date',
               'SOW Bill Rate (Daily)',
               'Date',
               'Actual Onboarding date',
               'Onbording Status',
               'Release Date',
               'BGV Status',
               'Credit Check',
               'DC Status',
               'SOW Request Sent ByHSBC Manager)',
               'SOW Approved By HSBC Manager',
               'SOW Sent By Procurement',
               'SOW Approved By Procurement',
               'HSBC Onboarding Kit',
               'SOW Status'
               ]

    def handle(self, *args, **options):
        values = ['resource_request__id',
                  'resource__BGV_status',
                  'resource__DC_status',
                  'resource__BGV_credit_check_status',
                  'resource__employee_name',
                  'resource__employee_id',
                  'resource__primary_skills__name',
                  'resource__is_external',
                  'selection_status',
                  'resource_request__location__name',
                  'selection_date',
                  'resource_request__department__name',
                  'resource_request__sub_department__name',
                  'resource_request__RR',
                  'resource_request__job_code',
                  'resource_request__SPOC__name',
                  'resource_request__synechron_contact',
                  'resource_request__client_group_head',
                  'resource_request__hiring_manager',
                  'resource_request__requestor',
                  'selection_role',
                  'on_boarding_kit',
                  'onbording_status',
                  'onboarding_date',
                  'release_date']
        rows = list(Candidature.objects.for_report().values(*values))
        #rows = rows+list(Candidature.objects.released().values(*values))
        #rows = rows+list(Candidature.objects.selected().values(*values))
        #rows = list(frozenset(rows))
        for r in rows:

            r['approval_received_from_procurement'] = r['SOW_sent_date_to_procurement'] = r['approval_received_from_account_manager'] = r[
                'sow'] = r['sow_start_date'] = r['bill_rate'] = r['sow_end_date'] = r['sow_status'] = r['SOW_sent_date_to_account_manager'] = ''
            if ResourceRequest.objects.get(pk=r['resource_request__id']).sows.all().count() > 0:
                r['sow'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].SOW_ID
                r['sow_start_date'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].start_date
                r['bill_rate'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].bill_rate
                r['sow_end_date'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].end_date
                r['sow_status'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].status
                r['SOW_sent_date_to_account_manager'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].SOW_sent_date_to_account_manager
                r['approval_received_from_account_manager'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].approval_received_from_account_manager
                r['SOW_sent_date_to_procurement'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].SOW_sent_date_to_procurement
                r['approval_received_from_procurement'] = ResourceRequest.objects.get(
                    pk=r['resource_request__id']).sows.all()[0].approval_received_from_procurement

        if self.export_to_excel is False:
            self.db = connect_database_server()
            self.cursor = self.db.cursor()
            create_database(self.cursor, self.db_name)
            create_table(self.cursor, self.table_name, self.columns)
        if self.export_to_excel is True:
            o = create_excel_sheet(self.table_name, self.columns)
            self.wb = o['wb']
            self.ws = o['ws']
        ri = 1
        for row in rows:
            new_vals = [ri,
                        row['resource__employee_id'],
                        row['resource__employee_name'],
                        row['selection_status'],
                        row['selection_status'],
                        "INTERNAL" if row[
                            'resource__is_external'] == False else "EXTERNAL",
                        row['resource_request__location__name'],
                        row['selection_date'],
                        row['resource_request__department__name'],
                        row['resource_request__sub_department__name'],
                        row['resource__primary_skills__name'],
                        row['resource_request__RR'],
                        row['resource_request__job_code'],
                        row['sow'],
                        row['resource_request__SPOC__name'],
                        row['resource_request__synechron_contact'],
                        row['resource_request__client_group_head'],
                        row['resource_request__hiring_manager'],
                        row['resource_request__requestor'],
                        '',
                        row['selection_role'],
                        row['sow_start_date'],
                        row['sow_end_date'],
                        row['bill_rate'],
                        row['onboarding_date'],
                        row['onboarding_date'],
                        row['onbording_status'],
                        row['release_date'],
                        row['resource__BGV_status'],
                        row['resource__BGV_credit_check_status'],
                        row['resource__DC_status'],
                        row['SOW_sent_date_to_account_manager'],
                        row['approval_received_from_account_manager'],
                        row['SOW_sent_date_to_procurement'],
                        row['approval_received_from_procurement'],
                        row['on_boarding_kit'],
                        row['sow_status']
                        ]
            if self.export_to_excel is False:
                insert_into_table(self.cursor, self.table_name, new_vals)
            else:
                if row['onbording_status'] == 'Released':
                    new_vals1=copy.deepcopy(new_vals)
                    new_vals1[self.columns.index('Onbording Status')]='No'
                    insert_to_excel(self.ws, self.columns, ri, new_vals1)
                    ri=ri+1
                    new_vals1[self.columns.index('Onbording Status')]='Yes'
                    insert_to_excel(self.ws, self.columns, ri, new_vals1)
                    ri=ri+1
                if row['onbording_status'] == 'Yes':
                    new_vals1=copy.deepcopy(new_vals)
                    new_vals1[self.columns.index('Onbording Status')]='No'
                    insert_to_excel(self.ws, self.columns, ri, new_vals1)
                    ri=ri+1
                    #insert_to_excel(self.ws, self.columns, ri, new_vals)
                insert_to_excel(self.ws, self.columns, ri, new_vals)
            ri = ri+1

        if self.export_to_excel is False:
            self.cursor.close()
            # Commit your changes in the database
            self.db.commit()

            # disconnect from server
            self.db.close()
        else:
            save_to_reports_folder(self.wb, self.table_name)
