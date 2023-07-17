from sqlite3 import Cursor
from unittest import result
from webbrowser import get
import pyodbc
from django.conf import settings
from casestudy.cognitivesearch import runindexer
import os 
from dotenv import load_dotenv
load_dotenv()
#connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:dlpractice.database.windows.net,1433;Database=DL-practice;Uid=admin123;Pwd=Admin@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
connection_string=os.getenv("CONNECTION_STRING")
connection = pyodbc.connect(connection_string)
#Driver={ODBC Driver 17 for SQL Server};Server=tcp:case-study-poc.database.windows.net,1433;Database=case-study-db;Uid=dbadmin;Pwd=db@admin12345;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
def get_file(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor= connection.cursor()
        result=cursor.execute(f"select FileName from [dbo].[case_studies] where id={id}")
        result=cursor.fetchone()
        file_name = result[0] if result else None
        cursor.close()
        return file_name
    except Exception as e:
        print(f"file name not found:{e}")
def get_file2(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor= connection.cursor()
        result=cursor.execute(f"select name from [dbo].[artifacts] where id={id}")
        result=cursor.fetchone()
        file_name = result[0] if result else None
        cursor.close()
        return file_name
    except Exception as e:
        print(f"file name not found:{e}")
def add_data(name,account,vertical,spoc,solution,service_offering_mapping,status,metadata,filename,rating,year,casestudy_poc,customer_reference,dependency):
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        query=f"Insert into [dbo].[case_studies](CaseStudyName,Account,Vertical"\
            f",SolutionName,ServiceOfferingMapping,Status,Dependency,MetaData,FileName,Rating,Year,CaseStudyPOC,CustomerReferenceable,spoc) values"\
            f"('{name}','{account}','{vertical}','{solution}','{service_offering_mapping}','{status}','{dependency}','{metadata}','{filename}','{rating}','{year}','{casestudy_poc}','{customer_reference}','{spoc}')"
        cursor.execute(query)
        connection.commit()
        runindexer.runindex()
        runindexer.run_azureblobindexer()
        cursor.close()
        #print("adding data here")
        
    except Exception as e:
        print(f"Error occured:{e}")
#def update_data(id, name, account, vertical, solution, sof, status, dep, remarks, meta, file, rating):
def update_data(id, name, account, vertical, spo, solution, service_offering_mapping, status, metadata, filename, rating, year, casestudy_poc, customer_reference, dependency):
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        query=f"UPDATE [dbo].[case_studies] SET CaseStudyName='{name}', Account='{account}', Vertical='{vertical}', " \
                f"SolutionName='{solution}', ServiceOfferingMapping='{service_offering_mapping}', Status='{status}', Dependency='{dependency}', " \
                f" MetaData='{metadata}', FileName='{filename}', Rating='{rating}',spoc='{spo}',Year='{year}',CaseStudyPOC='{casestudy_poc}',CustomerReferenceable='{customer_reference}' WHERE id={id}"
        cursor.execute(query)
        connection.commit()
        runindexer.runindex()
        runindexer.run_azureblobindexer()
        cursor.close()
        #print("Updated")
        
    except Exception as e:
        print(f"Error occured: {e}")

def get_row(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        query=f"select * from [dbo].[case_studies] where id={id}"
        result=cursor.execute(query)
        result=cursor.fetchone()
        result=result if result else None
        connection.commit()
        cursor.close()
        return result
    except Exception as e:
        print(f"error occured:{e}")
def get_all():
    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:case-study-poc.database.windows.net,1433;Database=case-study-db;Uid=dbadmin;Pwd=db@admin12345;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Pooling=True;')
    cursor= connection.cursor()
    try:
        result=cursor.execute(f"select * from [dbo].[case_studies]")
        result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        connection.commit()
        cursor.close()
        return serializable_data
    except Exception as e:
        print(f"error occured:{e}")

def getaiFiltereddata(filename):
    
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute(f"select * from  [dbo].[case_studies] where FileName='{filename}'")
        result=result.fetchone()
        if result:
            column_names = [column[0] for column in cursor.description]  # Get column names
            data = dict(zip(column_names, result))  # Convert the row to a dictionary
            return data
    except Exception as e:
        print(f"error occured at {e}")

def get_user():
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute(f"select * from [dbo].[Users] where where Is_Active='true'")
        result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        return serializable_data
    except Exception as e:
        print(f"error occured at {e}")
def get_user(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute(f"select * from [dbo].[Users] where id={id}")
        result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        return serializable_data
    except Exception as e:
        print(f"error occured at {e}")
def get_users():
    try:
        connection = pyodbc.connect(connection_string)
        cursor= connection.cursor()
        result=cursor.execute(f"select * from [dbo].[Users] where Is_Active='true'")
        result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        return serializable_data
    except Exception as e:
        print(f"error occured:{e}")
    
def get_accounts():
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute("select value,label from [dbo].[accounts]")
        result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        connection.commit()
        cursor.close()
        return serializable_data
    except Exception as e:
        print(f"error occured:{e}")
def get_acounts2(vertical):
    
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute(f"select value,label from [dbo].[accounts] where vertical='{vertical}'").fetchall()
        #result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        connection.commit()
        cursor.close()
        return serializable_data
    except Exception as e:
        print(f"error occured:{e}")


def audit_logs():
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute(f"select * from [dbo].[Track]")
        result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        return serializable_data
    except Exception as e:
        print(f"error occured at {e}")
def add_users(name,email,status):
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        cursor.execute(f"insert into [dbo].[Users] (Name,Email,Is_Active,Access_Level) values('{name}','{email}','true','{status}')")
        connection.commit()
        cursor.close()
    except  Exception as e:
        print(f"error occured at {e}")
"""def track(name,email,time,id):
    cursor=connection.cursro()
    try:
        cursor.execute(f"insert into [dbo].[Track] values('{name}','{email}','{time}',{id})")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"error occured at {e}") """
def change_access_level(status,id):
    cursor=connection.cursor()
    try:
        cursor.execute(f"update [dbo].[Users] set Access_Level='{status}' where id={id}")
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"error occured at {e}")
def softDelete(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        cursor.execute(f"update [dbo].[Users] set Is_Active='false' where id={id}")
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"error occured at {e}")
"""def active_user(email):
    cursor=connection.cursor()
    try:
        cursor.execute(f"select Is_Active from [dbo].[Users] where Email='{email}")
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"error occured at {e}") """
def user_status(email):
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute(f"select Access_Level from [dbo].[Users] where Email='{email}")
        return result.fetchone()
    except Exception as e:
        print(f"error occured at {e}")


def get_artifacts():
    try:
        connection = pyodbc.connect(connection_string)
        cursor=connection.cursor()
        result=cursor.execute("select * from [dbo].[artifacts]")
        result=result.fetchall()
        serializable_data= [dict(zip([column[0] for column in cursor.description],row)) for row in result]
        connection.commit()
        return serializable_data
    except Exception as e:
        print(f"error occured at {e}")