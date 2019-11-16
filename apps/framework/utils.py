from django.conf import settings
import MySQLdb
import xlwt
import datetime
server = settings.DATABASES['default']['HOST']
db_user = settings.DATABASES['default']['USER']
db_password = settings.DATABASES['default']['PASSWORD']


def connect_database_server():
    db = MySQLdb.connect(server, db_user, db_password)
    return db


def create_database(cusrsor, db_name):
    cusrsor.execute("create database IF NOT EXISTS " + db_name)
    cusrsor.execute("use " + db_name)


def create_table(cursor, table_name, list):
    str = ''
    for key in list:
        str = str + "`" + key + "`" + ' varchar(100),'
    str = str[:-1]
    statement = "drop table IF  EXISTS " + table_name+" ;"
    cursor.execute(statement)
    statement = "create table IF NOT EXISTS " + table_name + "(" + str + ");"
    cursor.execute(statement)
    statement = "delete from " + table_name+" ;"
    cursor.execute(statement)
    print statement


def insert_into_table(cursor, table_name, list):
    st = ''.encode("utf8")
    for val in list:
        val = str(val).replace("'", "''")
        st = st+"'" + str(val) + "'"+' ,'
    st = st[:-1]
    sql_statement = "insert into " + table_name + " values(" + st + " )"
    sql_statement = sql_statement.replace("didn't join", "did not join")
    cursor.execute(sql_statement)


def create_excel_sheet(sheet_name, columns):

    wb = xlwt.Workbook(encoding='utf-8')

    ws = wb.add_sheet(sheet_name)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    return {'wb': wb, 'ws': ws}


def insert_to_excel(ws, columns, ri, row):
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'
    for col_num in range(len(columns)):
        if isinstance(row[col_num], datetime.date):
            ws.write(ri, col_num, row[col_num], date_format)
        else:
            ws.write(ri, col_num, row[col_num], font_style)


def save_to_reports_folder(wb, table_name):
    name = settings.REPORTS_ROOT+'/'+table_name+'.xls'
    wb.save(name)
