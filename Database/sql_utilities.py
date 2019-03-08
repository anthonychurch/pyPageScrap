from collections import OrderedDict
import re

def encase_in_quotes(arg,type):
	if type == '"':
		arg = '"' + arg + '"'
	if type == '`':
		arg = '`' + arg + '`'
	else:
		arg = "'" + arg + "'"
	return arg
	
def get_max_column_value_string(column,table):
	max = "SELECT MAX(" + column + ") AS maxnum FROM " + table;
	return max

'''
This function constructs the SQL command to create a new table
Column is a key/value array:
key = name of the DB column
value = DB datatype time and length e.g INT or VARCHAR(50)
SQL syntax CREATE TABLE table (column1 datatype, column2 datatype, ..... )
	
Example of create table statement:
	
USE `products`

CREATE TABLE IF NOT EXISTS `products` (
	`productID` INT NOT NULL,
	`productName` VARCHAR(64),
	 PRIMARY KEY (`productID`)
)

CREATE TABLE IF NOT EXISTS `customers` (
	`customerID` INT NOT NULL AUTO_INCREMENT,
	`customertName` VARCHAR(64),
	 PRIMARY KEY (`customerID`)
)

#To allow for the naming of foriegn keys, use the following commands
CREATE TABLE IF NOT EXISTS `Orders` (
	`orderID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`orderNumber` INT,
	`productID` INT,
	`customerID` INT,
    CONSTRAINT `FK_productID` FOREIGN KEY (`productID`)
    REFERENCES products(`productID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    CONSTRAINT `FK_customerID` FOREIGN KEY (`customerID`)
    REFERENCES customers(`customerID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
)
	
The structure of a table dictionary: 
VAR_DICTIONARY_NAME = 
{
	'table' :  
		{
			'table_name' :
				{
					# Table columns and their values
					'id' :
						{
							'columnID' : 'datatype'
						}
					'columns' :
						{
							'column' : 'datatype', 
							'column' : 'datatype', 
							........
						}
				}
		}, 
	'fk' :
			{
			'table_name' :
				{
					'id' :
						{ 
							'columnID' : 'datatype' 
							# NOTE: 'columnID' name should equal the name of 'column' 
							# in the table dictionary that is going to be the foreign key to
						}
					'columns' :
						{ 
							'column' : 'datatype' 
						}
				},
			'table_name' : 
				{
					'id' :
						{ 
							'columnID' : 'datatype' 
						}
					'columns' :
						{
							'column' : 'datatype',
							'column' : 'datatype',
							...........
						}
				}
			}
		........
}
'''
def create_table_string(tableName,columns,foreignKeys):
	# Add Foriegn Keys keywords
	conName = "CONSTRAINT "
	conFK = " FOREIGN KEY ("
	conRef = ") REFERENCES "
	conEnd = ") ON DELETE SET NULL ON UPDATE CASCADE, "
	
	#tableName = table.keys()[0] # Retreives the table name ('table' key)
	#columnDict = columns.values() # Retreives the dictionary value of 'table' key 

	returnString = 'CREATE TABLE IF NOT EXISTS ' + encase_in_quotes(tableName,'`') + ' ( '
		
	# Concatenate the key and values to the returnString variable
	for c in columns.items():
		# Add to the the returnstring by adding data from the ID and columns dictionaries
		for k,v in c[1].items():
			returnString += encase_in_quotes(k,'`') + ' ' + v + ', '

	#print returnString
	
	if foreignKeys is not None:
		for fk in foreignKeys.items():
			# Get FK table name
			fkTable = fk[0]
			# Add CONSTRAINT key word
			returnString += conName
			# Get the column name that is going to have the foreign key attached to it
			# NOTE: 'columnID' name should equal the name of 'column' in the 
			#       table dictionary that is going to be the foreign key to
			fkID = fk[1]['id'].keys()[0] 
			# Name and create fk constraint form column
			returnString += encase_in_quotes('FK_'+ fkID,'`') + conFK + encase_in_quotes(fkID,'`')
			# Add fk reference
			returnString += conRef + fkTable + "(" + encase_in_quotes(fkID,'`') + conEnd
	
	# Remove end comma	
	returnString = returnString[0:len(returnString)-2]
	
	return returnString + ' )'

'''	
def insert_kv_into_table_string(tableName,kwargs):
	returnString = "INSERT INTO " + encase_in_quotes(str(tableName),'`')
	columnString = "("
	valueString = "("
	for k,v in kwargs.items():
		columnString += encase_in_quotes(str(k),'`') + ', '
		valueString += encase_in_quotes(str(v),"'") + ', '
		
	columnString = columnString[0:len(columnString)-2]
	columnString += ")"
	valueString = valueString[0:len(valueString)-2]
	valueString += ")"
	
	returnString += columnString + " VALUES " + valueString
	
	return returnString
'''	

'''
def insert_kv_into_table_string(database,tableName,id,idValue,kwargs):
database = database
tableName = name of the table that the data in the kwargs var are to be injected into
id = is the mysql id type for the table
idValue = is the mysql id type's value
kwargs = unspecified size of key/value array items
'''
def insert_kv_into_table_string(database,tableName,id,idValue,kwargs):
	returnString = "INSERT INTO " + encase_in_quotes(str(database),'`') + '.' + encase_in_quotes(str(tableName),'`')
	columnString = "("
	valueString = "("
	columnString += encase_in_quotes(str(id),'`') + ', '
	valueString += encase_in_quotes(str(idValue),"'") + ', '
	for k,v in kwargs.items():
		columnString += encase_in_quotes(str(k),'`') + ', '
		valueString += encase_in_quotes(str(v),"'") + ', '
		
	columnString = columnString[0:len(columnString)-2]
	columnString += ")"
	valueString = valueString[0:len(valueString)-2]
	valueString += ")"
	
	returnString += columnString + " VALUES " + valueString
	
	return returnString
	
	
def check_if_column_exists_in_table_string(database,tableName,column):
	returnString = 'SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = ' + encase_in_quotes(str(database),"'")
	returnString += 'AND TABLE_NAME = ' + encase_in_quotes(str(tableName),"'")
	returnString += ' AND COLUMN_NAME = ' + encase_in_quotes(str(column),"'")
	return returnString
'''
def add_column_to_table_string(database,tableName,column,datatype):
	returnString = 'ALTER TABLE ' + encase_in_quotes(str(database),"'") + '.' + encase_in_quotes(str(tableName),"'")
	returnString += ' ADD ' + encase_in_quotes(str(column),"'") + ' ' + encase_in_quotes(str(datatype),"'")
	return returnString
'''	
def add_column_to_table_string(database,tableName,column,datatype):
	returnString = 'ALTER TABLE ' + database + '.' + tableName
	returnString += ' ADD ' + column + ' ' + datatype
	return returnString
