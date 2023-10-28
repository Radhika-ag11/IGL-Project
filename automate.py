import pandas as pd
import cx_Oracle
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine

#Query to execute
query = ''' select SYSTIMESTAMP, fs.tablespace_name "Tablespace",(df.totalspace - fs.freespace)"Used MB",
            fs.freespace"Free MB",df.totalspace"Total MB",round(100 * (fs.freespace / df.totalspace)) "Pct. Free"
            from(select tablespace_name,round(sum(bytes) / 1048576) TotalSpace from dba_data_files group by tablespace_name) df, 
            (select tablespace_name, round(sum(bytes) / 1048576) FreeSpace from dba_free_space group by tablespace_name ) fs 
            where df.tablespace_name = fs.tablespace_name'''
totalSpace_query='select SYSTIMESTAMP, sum(bytes)/1024/1024/1024/1024 size_in_mb from dba_data_files'

# Oracle connection details
oracle_username = 'xxxx'
oracle_password = 'xxxx'
oracle_port = '1521' #default port

oracle_PRDOTDB_service_name = 'ECMPRDDB'
oracle_PRDOTDB_hostname = 'PRDOTDB'

#Add more here

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="xxxx",
                               db="dbstorage"))

def retrieve_and_save_size(): 
    #set connection to oracle
    PRDOTDB_dsn = cx_Oracle.makedsn(oracle_PRDOTDB_hostname, oracle_port, service_name=oracle_PRDOTDB_service_name)
    PRDOTDB_connection = cx_Oracle.connect(oracle_username, oracle_password, PRDOTDB_dsn)

    PRDOTDB_cursor = PRDOTDB_connection.cursor()
    PRDOTDB_cursor_exec=PRDOTDB_cursor.execute(query)
    PRDOTDB_df= pd.DataFrame(PRDOTDB_cursor_exec, columns = ['Time','Table_SpaceName','UsedSpace_in_MB','FreeSpace_in_MB','TotalSpace_in_MB','Percentage_Free'])
    PRDOTDB_df.to_sql('DBinformation',con=engine, if_exists = 'append',index = False, chunksize = 1000)

    PRDOTDB_total_cursor = PRDOTDB_connection.cursor()
    PRDOTDB_total_cursor_exec=PRDOTDB_total_cursor.execute(totalSpace_query)
    PRDOTDB_total_df= pd.DataFrame(PRDOTDB_total_cursor_exec, columns = ['Time','TotalSpace_in_TB'])
    PRDOTDB_total_df.to_sql('total_space',con=engine, if_exists = 'append',index = False, chunksize = 1000)

    PRDOTDB_cursor.close()
    PRDOTDB_connection.close()

if __name__ == "__main__":
    retrieve_and_save_size()


