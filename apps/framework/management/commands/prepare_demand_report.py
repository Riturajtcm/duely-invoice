from django.core.management.base import BaseCommand
from account_master.models import *
from location_master.models import *
from skill_master.models import *
from demand_master.models import *
from framework.utils import *
import sys
from collections import OrderedDict
import hashlib


class Command(BaseCommand):
    help = 'Exports All customers Data'
    db_name = 'pmo_reports'
    table_name = 'demand_status'
    export_to_excel = True
    columns = ['SR',
               'RR #',
               'Job Code',
               'Tech/Skill',
               'Technology',
               'Department',
               'Sub-Department',
               'Requestor',
               'Status',
               'Location',
               'Req published Date',
               'Ageing',
               "No. of Profiles Sent to HSBC",
               "No of Profiles Interviewed",
               "Selection Status",
               "Candiadte Selection Date",
               "Emp Id",
               "Name of Selected Resource",
               "Proposed Date of Joining",
               "DC Cleared",
               "BGV Cleared",
               "SOW signed",
               "Onboarded",
               "Date of Actual Joining",
               "Abort",
               "Delayed",
               "Reason for Abort or Delay",
               "Remarks if any",
               "Role",
               "HSBC Priority",
               "Requisition #",
               "Program Total",
               "Open",
               "Closed",
               "On Hold",
               "Demand Cancelled",
               "Profiles",
               "Interviewed",
               "Profiles Sent Date",
               "L1 Interview Date",
               "L1 Interview Status",
               "L2 Interview Date",
               "L2 Interview Status",
               "Enhanced Status",
               "Remarks",
               "Must start by date",
               "RAG",
               "Last Updated",
               "Profile Sent Aging",
               "Synechron POC",
               ]

    def handle(self, *args, **options):
        reload(sys)
        sys.setdefaultencoding('utf8')
        if self.export_to_excel is False:
            self.db = connect_database_server()
            self.cursor = self.db.cursor()
            create_database(self.cursor, self.db_name)
            create_table(self.cursor, self.table_name, self.columns)
        if self.export_to_excel is True:
            o = create_excel_sheet(self.table_name, self.columns)
            self.wb = o['wb']
            self.ws = o['ws']
        rows = ResourceRequest.objects.all()
        output = []
        for demand in rows:
            candidatures = demand.candidatures.all()
            for candidature in candidatures:
                resource = candidature.resource
                row = OrderedDict()
                row['RR'] = demand.RR
                row['job_code'] = demand.job_code
                row['tech_skills'] = demand.tech_skills
                row['technology'] = demand.technology.name
                row['department'] = demand.department.name \
                    if demand.department \
                    is not None else ""
                row['sub_department'] = demand.sub_department.name\
                    if demand.sub_department is not None else ""
                row['requestor'] = demand.requestor
                row['status'] = demand.demand_status
                row['location'] = demand.location.name \
                    if demand.location is not None else ""
                row['request_publish_date'] = demand.request_receive_date
                row['aging'] = demand.age()
                row['number_of_profile_send'] = candidatures.count()
                row['number_of_profile_interviewed'] = candidatures.count()
                row['selection_status'] = demand.demand_status
                row['selection_date'] = candidature.selection_date \
                    if candidature.selection_date is not None else ""
                row['emp_id'] = resource.employee_id \
                    if resource is not None else ""
                row['emp_name'] = resource.employee_name \
                    if resource is not None else ""
                row['preposed_date_of_joining'] = candidature.onboarding_date
                row['dc_status'] = resource.DC_status \
                    if resource is not None else ""
                row['bgv_status'] = resource.BGV_status \
                    if resource is not None else ""
                row['sow_signed'] = demand.get_sow(
                ).status if demand.get_sow(
                ) is not None else ""
                row['onboarded'] = candidature.onbording_status
                row['date_of_actual_joining'] = candidature.actual_start_date \
                    if candidature.actual_start_date is not None else ""
                row['abort'] = ""
                row['delayed'] = ""
                row['Reason_for_Abort_or_Delay'] = candidature.remarks
                row['Remarksifany'] = candidature.remarks
                row['role'] = candidature.selection_role
                row['HSBC_priority'] = ""
                m = hashlib.new('ripemd160')
                requisition = '{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12}'.format(
                    demand.created_on,
                    demand.requestor,
                    demand.SPOC,
                    demand.technology_id,
                    demand.sub_department_id,
                    demand.requisition_id,
                    demand.technology_id,
                    demand.tech_skills,
                    demand.hiring_manager,
                    demand.client_group_head,
                    demand.created_by_id,
                    demand.project_name,
                    demand.synechron_contact,
                    demand.request_receive_date
                )
                m.update(requisition)
                row['requisition'] = m.hexdigest()
                row['total'] = ""
                row['open'] = ""
                row['closed'] = ""
                row['on_hold'] = ""
                row['demand_cancelled'] = ""
                row['Profiles'] = ""
                row['Interviewed'] = ""
                row['ProfilesSentDate'] = candidature.profile_submittion_date
                row['L1InterviewDate'] = candidature.interview_date
                row['L1InterviewStatus'] = candidature.selection_status
                row['L2InterviewDate'] = candidature.L2_interview_date
                row['L2InterviewStatus'] = candidature.L2_interview_date
                row['EnhancedStatus'] = ""
                row['Remarks'] = ""
                row['Must_start_by_date'] = ""
                row['RAG'] = ""
                row['Last_Updated_on'] = ""
                row['profile_send_aging'] = ""
                row['Synechron POC'] = demand.SPOC.name
                output.append(row)
        ri = 1
        if self.export_to_excel is False:
            for o in output:
                new_vals = [ri]+o.values()

                insert_into_table(self.cursor, self.table_name, new_vals)
                ri = ri+1
                # Commit your changes in the database
            self.db.commit()
            self.cursor.close()
            # disconnect from server
            self.db.close()
        else:
            for o in output:
                new_vals = [ri]+o.values()
                insert_to_excel(self.ws, self.columns, ri, new_vals)
                ri = ri+1
            save_to_reports_folder(self.wb, self.table_name)
