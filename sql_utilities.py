""" 

This function constructs the SQL command to create a new table
Column is a key/value array:
key = name of the DB column
value = DB datatype time and length e.g INT or VARCHAR(50)
SQL syntax CREATE TABLE table (column1 datatype, column2 datatype, ..... )
	
Example of create table statement:
	
CREATE TABLE Orders (
	orderID INT NOT NULL,
	orderNumber INT NOT NULL,
	product INT,
	customer INT,
	PRIMARY KEY (orderID),
	CONSTRAINT FK_product FOREIGN KEY (product)
	REFERENCES products(productID),
	CONSTRAINT FK_customer FOREIGN KEY (customer)
	REFERENCES customers(customerID)
)
	
The structure of the columns dictionary: { 'column1':'datatype', 'column2':'datatype' ) 
		
The structure of the foreignKeys dictionary: { 'fkTable1':{'fkColumn':'column1'}, 'fkTable2':{'fkColumn':'column2'} ) 

"""


def getDBcreateTableString(table, columns, foreignKeys):
	# Add Foriegn Keys keywords
	conName = "CONSTRAINT "
	conFK = " FOREIGN KEY ("
	conRef = ") REFERENCES "
	conEnd = ") ON DELETE SET NULL ON UPDATE CASCADE, "

	returnString = 'CREATE TABLE IF NOT EXISTS ' + table + ' ( '
	
	# Concatenate the key and values to the returnString variable
	for k,v in columns.items():
		returnString += k + ' ' + v + ', '

	if foreignKeys is not None:
		# Get first dictionary element
		for s,t in foreignKeys.items():
			# Add CONSTRAINT key word
			returnString += conName
			# Get second dictionary elements
			for k,v in t.items():
				# Name and create fk constraint form column
				returnString += 'FK_'+ v + conFK + v
				# Add fk reference
				returnString += conRef + s + '(' + k + conEnd
		
	# Remove end comma	
	returnString = returnString[0:len(returnString)-2]

	return returnString + ' )'	
	