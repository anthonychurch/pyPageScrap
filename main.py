from Database import *
from Database import TABLE_PROD_TV_SERIES
from Database import DB_CONNECT
from Database import sql_utilities as su
import pymysql

# Get connection data securely
host = DB_CONNECT['host']
port = DB_CONNECT['port']
user = DB_CONNECT['user']
password = DB_CONNECT['password']

# Connect to DB and get cursor object
conn = pymysql.connect(host=host, port=port, user=user, passwd=password)
cur = conn.cursor()

'''
Check to see if TABLES_PROD_TV_SERIES has foreign keys 
if so create tables that contain the foreign key data if they do not exist
'''
if TABLE_PROD_TV_SERIES['fk'] is not None:
	fk = TABLE_PROD_TV_SERIES['fk']
	table = None
	
	# Iterate through the 'fk' dictionary
	'''
	fk dictionary structure = fk : { table : {column : datatype, column : datatype},  table : {column : datatype, column : datatype}, .... } 
	therefore fk[0] = table and fk[1] = {column : datatype, column : datatype}
	'''
	for i in fk.items():
		# Iterate through i dictionary and get the key and values of the second index in i
		table = i[0][1:len(i[0])]
		print su.getDBcreateTableString(table, i[1], None)

cur.close()
conn.close()




