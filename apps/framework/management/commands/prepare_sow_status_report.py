from django.core.management.base import BaseCommand
from account_master.models import *
from location_master.models import *
from skill_master.models import *
from candidature_master.models import *
from resource_master.models import *
from candidature_master.models import *
from sow_master.models import *
from framework.utils import *


class Command(BaseCommand):
    help = 'Exports All customers Data'
    db_name = 'pmo_reports'
    table_name = 'sow_status'
    export_to_excel = True
    columns = ['Sr.No',
               'Approval Received',
               'Project Name',
               'SOW Location',
               'SOW #',
               'Previous SOW #',
               'PO Number ',
               'Status',
               'Client Group Head',
               'HSBC Line Manager',
               'Requestor',
               'Synechron SPOC',
               'Synechron Contact',
               'HSBC Department',
               'HSBC Sub Department',
               'Payment Terms',
               'SoW Start Date',
               'SoW end Date',
               'SoW Value USD',
               'SoW  Resources#',
               'Actual Onsite#',
               'Total Bill Rate in SOW',
               '2016 Commited Spend days',
               '2017 Commited Spend days',
               '2018 Commited Spend days',
               'SOW Sent To Client manager',
               'SOW Received From Client manager',
               'SOW Sent To Procurement',
               'SOW Received Procurement',
               ]

    def handle(self, *args, **options):
        if self.export_to_excel is False:
            self.db = connect_database_server()
            self.cursor = self.db.cursor()
            create_database(self.cursor, self.db_name)
            create_table(self.cursor, self.table_name, self.columns)
        if self.export_to_excel is True:
            o = create_excel_sheet(self.table_name, self.columns)
            self.wb = o['wb']
            self.ws = o['ws']
        rows = SOW.objects.all().values('approval_received_from_procurement',
                                        'SOW_ID',
                                        'Previous_SOW_ID',
                                        'PO_number',
                                        'location__name',
                                        'status',
                                        'department__name',
                                        'line_manager',
                                        'start_date',
                                        'end_date',
                                        'payment_terms',
                                        'SOW_value',
                                        'bill_rate',
                                        'number_of_resources',
                                        'commited_spend_days_2016',
                                        'commited_spend_days_2017',
                                        'commited_spend_days_2018',
                                        'SOW_sent_date_to_account_manager',
                                        'approval_received_from_account_manager',
                                        'SOW_sent_date_to_procurement',
                                        'approval_received_from_procurement',
                                        )
        for r in rows:
            r['project_name'] = r['client_group_head'] = r['synechron_contact'] \
                = r['requestor'] = r['spoc'] = \
                r['sub_department'] = r['actual_onborded'] = ""
            sow = SOW.objects.all().filter(SOW_ID=r['SOW_ID'])
            if sow.count() is not 0:
                sow = SOW.objects.all().filter(SOW_ID=r['SOW_ID'])[0]
                if sow.resource_requests.count() > 0:
                    rr = sow.resource_requests.all()[0]
                    r['project_name'] = rr.project_name
                    r['client_group_head'] = rr.client_group_head
                    r['synechron_contact'] = rr.synechron_contact
                    r['requestor'] = rr.requestor
                    r['spoc'] = rr.SPOC.name
                    r['sub_department'] = rr.sub_department.name
                    r['actual_onborded'] = sow.resource_requests.filter(
                        demand_status='Deployed').count()

        ri = 1
        for row in rows:
            new_vals = [ri,
                        row['approval_received_from_procurement'],
                        row['project_name'],
                        row['location__name'],
                        row['SOW_ID'],
                        row['Previous_SOW_ID'],
                        row['PO_number'],
                        row['status'],
                        row['client_group_head'],
                        row['line_manager'],
                        row['requestor'],
                        row['spoc'],
                        row['synechron_contact'],
                        row['department__name'],
                        row['sub_department'],
                        row['payment_terms'],
                        row['start_date'],
                        row['end_date'],
                        row['SOW_value'],
                        row['number_of_resources'],
                        row['actual_onborded'],
                        row['bill_rate'],
                        row['commited_spend_days_2016'],
                        row['commited_spend_days_2017'],
                        row['commited_spend_days_2018'],
                        row['SOW_sent_date_to_account_manager'],
                        row['approval_received_from_account_manager'],
                        row['SOW_sent_date_to_procurement'],
                        row['approval_received_from_procurement']
                        ]
            if self.export_to_excel is False:
                insert_into_table(self.cursor, self.table_name, new_vals)
            else:
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
