from django.core.management.base import BaseCommand, CommandError
from account_master.models import *
from location_master.models import *
from skill_master.models import *
from demand_master.models import *
from candidature_master.models import *
from resource_master.models import *
from candidature_master.models import *
from .prepare_on_boarding_report import *
from framework.utils import *


class Command(BaseCommand):
    help = 'Exports All customers Data'
    db_name = 'pmo_reports'
    table_name = 'resource_reports'
    export_to_excel=True
    def handle(self, *args, **options):
        db_name = 'pmo_reports2'
        table_name = 'resource_reports'
        self.columns = ['SR','Month',
                        'Fiscal Quarter',
                        'Fiscal Year',
                        'Employee Id',
                        'DOJ',
                        'EMail ID',
                        'Account',
                        'Account Start Date',
                        'End date',
                        'Utilization(%)',
                        'Designation',
                        'Status',
                        'Role',
                        'Department',
                        'Project',
                        'Country',
                        'City',
                        'Emp Cost',
                        'Project start date',
                        'Project end date',
                        'SOW #',
                        'HSBC Line Manager',
                        'Synechron SPOC',
                        'HSBC Department',
                        'HSBC Sub Department',
                        'SoW Value USD'
                        ]

        rows = Resource.objects.all().values(
            'synechron_account__name',
            'employee_name',
            'employee_id',
            'email',
            'account_start_data',
            'account_release_date',
            'country__name',
            'city__name')
        for r in rows:
            candidature = None
            r['role'] = r['project_name'] = r[
                'project_start_date'] = r['project_end_date'] = ""
            r['sow'] = r['hsbc_line_manager'] = r[
                'spoc'] = r['hsbc_department'] = ""
            r['hsbc_sub_department'] = r['sow_value'] = ""
            candidatures = Candidature.objects.filter(resource__employee_id=r[
                                                      'employee_id'], selection_status='SELECTED').order_by('-last_moddified_on')
            if candidatures.count() > 0:
                candidature = candidatures[0]
            if candidature is not None:
                r['role'] = candidature.selection_role
                r['project_name'] = candidature.resource_request.project_name
                r['project_start_date'] = candidature.onboarding_date
                r['project_end_date'] = candidature.release_date
                r['selection_role'] = candidature.selection_role

                try:
                    r['sow'] = candidature.resource_request.sows.all()[
                        0].sow_id
                except Exception as e:
                    pass

                r['hsbc_line_manager'] = candidature.resource_request.hiring_manager
                r['spoc'] = candidature.resource_request.SPOC.name
                r['hsbc_department'] = candidature.resource_request.department.name
                try:
                    r['hsbc_sub_department'] = candidature.resource_request.sub_department.name
                except Exception as e:
                    pass

                try:
                    r['sow_value'] = candidature.resource_request.sows.all()[
                        0].sow_value
                except Exception as e:
                    pass

        if self.export_to_excel is False:
            self.db = connect_database_server()
            self.cursor = self.db.cursor()
            create_database(self.cursor, self.db_name)
            create_table(self.cursor, self.table_name, self.columns)
        if self.export_to_excel is True:
            o= create_excel_sheet(self.table_name,self.columns)
            self.wb=o['wb']
            self.ws=o['ws']
        ri = 1
        for row in rows:
            new_vals = [ri,"",
                        "",
                        "",
                        row['employee_id'],
                        "",
                        row['email'],
                        row['synechron_account__name'],
                        row['account_start_data'],
                        row['account_release_date'],
                        "",
                        "",
                        "ACTIVE" if row[
                            'account_release_date'] is None else "RELEASED",
                        row['role'],
                        "",
                        row['project_name'],
                        row['country__name'],
                        row['city__name'],
                        "",
                        row['project_start_date'],
                        row['project_end_date'],
                        row['sow'],
                        row['hsbc_line_manager'],
                        row['spoc'],
                        row['hsbc_department'],
                        row['hsbc_sub_department'],
                        row['sow_value'],
                        ]
            if self.export_to_excel is False:
                insert_into_table(self.cursor, self.table_name, new_vals)
            else:
                insert_to_excel(self.ws,self.columns,ri, new_vals)
            ri = ri+1
            
        if self.export_to_excel is False:   
            self.cursor.close()
            # Commit your changes in the database
            self.db.commit()

            # disconnect from server
            self.db.close()
        else:
            save_to_reports_folder(self.wb,self.table_name)

