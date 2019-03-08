from database import TABLE_PROD_TV_SERIES
from database import DB_CONNECT
from database import DB_PROD_TV_SERIES
from database import IMG_DIR_BASE
from database import sql_utilities as su

from pageScrape import pgeScrp_utilities as ps

import pymysql
import sys

import urllib

import os

import re

from lxml import html
from lxml import etree
import requests

# Get connection data securely
host = DB_CONNECT['host']
port = DB_CONNECT['port']
user = DB_CONNECT['user']
password = DB_CONNECT['password']

retailer = 'sanity'


remChars = ['~','`','!','@','#','$','%','^','&','*','(',')','-','_','=','+','{','[','}',']','|','\\',':',';',"'",'"',',','<','.','>','?','/'] # used to remove non alpha numeric characters
noChars = ["'",'^'] # used to allow single quotes to be added in a db's table field

# Connect to DB and get cursor object
conn = pymysql.connect(host=host, port=port, user=user, passwd=password)
if not conn:
	conn.close()
	sys.exit("ERROR : SQL CONNECTION : failed to connect to SQL server")

#Store the page data in the page variable
page = requests.get('http://www.sanity.com.au/specials/1542/')
print page
productCat = 'tv_series'
if not page:
	conn.close()
	sys.exit("ERROR : INTERNET CONNECTION : failed to connect to internet page")
	

db = DB_PROD_TV_SERIES

sql = 'CREATE DATABASE IF NOT EXISTS '  + DB_PROD_TV_SERIES
cur = conn.cursor()
cur.execute(sql)

sql_useDB = 'USE ' + DB_PROD_TV_SERIES
cur.execute(sql_useDB)

'''
Get the tv series table data to be used to create the tables 
NOTE: tv series table needs to be made up of 2 dictionaries; 'table' and 'fk'
'''
tableName = None
columns = None
foreignKeys = None

productTitle = 'productTitle'
productID = 'productID'
productPage = 'productPage'




'''
Test to see if all the fields exist in the tables

SELECT * 
FROM information_schema.COLUMNS 
WHERE 
	TABLE_SCHEMA = 'db_name' 
AND TABLE_NAME = 'table_name' 
AND COLUMN_NAME = 'column_name'
'''
def check_if_column_exists(database,table,k_v_dict):
	#from database import sql_utilities as su
	
	result = None
	for k,v in k_v_dict.items():
		sql = su.check_if_column_exists_in_table_string(database,table,k)
		cur.execute(sql)
		result = cur.fetchall()
			
		if len(result) == 0:
			
			#ALTER TABLE table_name ADD column_name datatype;
			
			sql = su.add_column_to_table_string(database,table,k,v)
			cur.execute(sql)
			result = conn.commit()
				
	return result

if TABLE_PROD_TV_SERIES['table'] is not None:
	tableName = TABLE_PROD_TV_SERIES['table'].keys()[0]
	columns = TABLE_PROD_TV_SERIES['table'].values()[0]

if TABLE_PROD_TV_SERIES['fk'] is not None:	
	foreignKeys = TABLE_PROD_TV_SERIES['fk']

column_id = TABLE_PROD_TV_SERIES['table'][tableName]['id'].keys()[0]
max_id = 0
#irint "id = " + str(id)


'''
Check to see if TABLES_PROD_TV_SERIES has foreign keys 
if so create tables that contain the foreign key data if they do not exist
'''
if foreignKeys is not None:
	# Iterate through the 'fk' dictionary
	for fk in foreignKeys.items():
		# fk[0] = table name
		# fk[1] = column data divided into 2 dictionaries 'id' and 'columns'
		# fk[1]['columns'].keys() = returns the key of the dictionary. 
		# This is the name of the DB field
		sql = su.create_table_string(fk[0], fk[1], None)
		cur.execute(sql)

		#Test to see if all the fields exist in the tables
		result = check_if_column_exists(db,fk[0],fk[1]['columns'])

		
'''
Create the main table.
Specify if the table has foreign keys
Function = create_table_string(tableName,columns,foreignKeys)
'''
if tableName is not None:
	sql = su.create_table_string(tableName,columns,foreignKeys)
	cur.execute(sql)
	
	#print 'columns = ' + str(columns['columns'])
	#Test to see if all the fields exist in the tables
	result = check_if_column_exists(db,tableName,columns['columns'])	
		
#Create a tree of elements from a string containing XML
elementTree = html.fromstring(page.content)

#Using xPath Expressions:
#1. get the href and title attribute values of all anchor tags that are the child of div tags containing the class "thumb-image"
#2. get the scr value of all image tags that are the child of div tags containing the class "thumb-image"
product_link = {}
title = {}
thumb_link = {}
#exists = {}

#productPage will get the product page from the "thumb-image" that contains all the data about the product
product_link['productPage'] = elementTree.xpath('//div[@class="thumb-image"]/a/@href')
#productTitle will get the product tile for all pages
title['productTitle'] = elementTree.xpath('//div[@class="thumb-image"]/a/@title')
#thumbImageLink get the http/https address of the thumb nail image to be downloaded
thumb_link['thumbImageLink'] = elementTree.xpath('//div[@class="thumb-image"]/a/img/@src')
#exists['exist'] = [0,0,0,0]
#print product_link
#print title
#print thumb_link

# Remove any single quote from the product title 
for c in noChars:
	for i in range(0,len(title['productTitle']),1):
		#test = title['productTitle'][i].find("'")
		test = title['productTitle'][i].find(c)
		
		if test != -1:
			replace = "\\" + c
			#print "replace = " + str(replace)
			title['productTitle'][i] = title['productTitle'][i].replace(c,replace)
			#title['productTitle'][i] = title['productTitle'][i].replace("'","&quot;")# Test


'''
# REFERENCE AND TESTING PURPOSES ONLY
product_link['productPage'] = ['1-1','2-2','3-3','4-4']
title['productTitle'] = ['noo','foo','goo','boo']#['1-5','2-6','3-7','4-8']
thumb_link['thumbImageLink'] = ['1-9','2-10','3-11','4-12']
#exists['exist'] = [0,0,0,0]
#print product_link
#print title
#print thumb_link
'''

'''	
Filters and sort through links, title and img, matching each criteria to each other:

Function = get_captured_data(start,prefix,padding,*argv)

*argv = a nested list of dictionaries whose index values are mapped to each other.
         The aim is to interate through each list and assign each mapped value to a list value, which is mapped to a key
		  EXAMPLE: {'key':['value1','value2,'value3','value4']}
start = is the next unused index number from the table that this data is to be injected into.
prefix = the string prefix for the key string in the output dictionary
padding = this the zero padding for the sufix of the key string
'''

'''
poo = file('F:/Work/python/log.txt','r')
for line in poo.readlines():
    print line
text_file = open("Output.txt", "w")
text_file.write("Purchase Amount: " 'TotalAmount')
text_file.close()
'''
content = ps.get_captured_data(0,'tvSeries_',10,title,thumb_link,product_link)
#print content.keys()
 
# Add downloaded as a later to test to see if the product is already store in DB
for k in content.keys():
	content[k]['downloaded'] = 0
	content[k]['retailer'] = retailer

	
'''
Check for and remove any items that already exist in the database
In this case, the key 'title' is going to be used to cross reference if it exists 

Step 1: Get all the titles from the m_products table and stor in an array
EXAMPLE: SELECT productTitle FROM `products`.`m_products`;

Check to make sure that 'productTitle' is a key in the TABLE_PROD_TV_SERIES dictionary.
Its location will be in the following:
TABLE_PROD_TV_SERIES = {
		'table' :  
			{
			'm_products' :
				{
					# Table columns and their values
					'id' :
						{
							'productID' : 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY'
						},
					'columns' :
						{
							'productTitle' : 'VARCH................
'''
# Test to see if the value of the variable productTitle exists in the TABLE_PROD_TV_SERIES dictionary
if productTitle in TABLE_PROD_TV_SERIES['table']['m_products']['columns'].keys():

	# Get all value of all the productTitle items stored in the DB
	sql = 'SELECT `' + productTitle + '` FROM `products`.`m_products`'
	cur.execute(sql)
	getProductTitles = cur.fetchall()
	
	if getProductTitles is not None:
		for p in getProductTitles:
			for k in content.keys():
				
				# Remove all non alpha numeric characters to allow for a more accurate comparison				
				test_p = p[0]
				test_k = content[k]['productTitle']
				
				for rc in remChars:
					test_p = test_p.replace(rc,'')
				
				for rc in remChars:
					test_k = test_k.replace(rc,'')

				# Need to call the first index ( p[0] ) as fetchall outputs ((key1,),(key1,),....
				'''
				if test_p == test_k:
					# Update the downloaded key to ensure that it is not saved to DB twice
					content[k]['downloaded'] = 1
					break
				'''	
				# Do a thorough comparions by doing a word search
				# Break the titles into lists
				split_p = test_p.split()
				split_k = test_k.split()
				
				imageName = ''
				for i in split_k:
					imageName += str(i) + '_'
				imageName = imageName[0:len(imageName)-1]
				content[k]['imageName'] = imageName
				
				size_p = len(split_p)
				# Declare a variable to record the matches and
				# use to compare against the length of titles
				matches = 0
				
				for sp in split_p:
					for sk in split_k:
						if sp == sk:
							matches += 1
			
				if matches == size_p:
					# Update the downloaded key to ensure that it is not saved to DB twice
					content[k]['downloaded'] = 1
					#print 'test_p = ' + test_p
					#print 'test_k = ' + test_k
					break
else:
	conn.close()
	sys.exit("ERROR : " + str(productTitle) + " is not in dictionary TABLE_PROD_TV_SERIES")


'''
Get the highest index value from TABLE_PROD_TV_SERIES table
	
Get the last Product ID entry in the m_Products table
'''
sql = su.get_max_column_value_string(column_id,tableName)
#print sql
cur.execute(sql)


getMaxId = cur.fetchall()[0][0]
# Test to see if getMaxId = None (table is empty of values)
# If so, make sure the table index starts at 1
if getMaxId == None:
	getMaxId = 0

	
'''
Store the data from the content variable into a database
EXAMPLE:
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);
'''

'''
def insert_kv_into_table_string(database,tableName,id,idValue,kwargs):
database = database
tableName = name of the table that the data in the kwargs var are to be injected into
id = is the mysql id type for the table
idValue = is the mysql id type's value
kwargs = unspecified size of key/value array items
'''
id = TABLE_PROD_TV_SERIES['table'][tableName]['id'].keys()[0]
idValue = getMaxId+1

# NOTE: product titles that have already been stored in the database have already been filtered out
# This indicated by the content[k]['downloaded'] being equal to 1
# If an product title dublicates are continually being added, check the comparison methodology under the 
# section "Test to see if the value of the variable productTitle exists in the TABLE_PROD_TV_SERIES dictionary"
for k in content.keys():
	if not content[k]['downloaded']:
		# def insert_kv_into_table_string(tableName,id,idValue,kwargs)
		sql = su.insert_kv_into_table_string(db,tableName,id,idValue,content[k])
		cur.execute(sql)
		conn.commit()
		idValue += 1

		
'''
Save the images associated with the product
'''
for k in content.keys():
	if content[k]['imageName']:
		name = content[k]['imageName']
		
		folder = IMG_DIR_BASE + '\\' + name
		# check if directory exists
		dirExist = os.path.isdir(folder)

		if not dirExist:
			os.makedirs(folder)
			
		if dirExist:
			splitLink =  content[k]['thumbImageLink'].split('/')
			getImageName = splitLink[-1]
			si = folder + '\\' + getImageName
			
			if not os.path.isfile(si):
				saveImage = urllib.URLopener()
				saveImage.retrieve(content[k]['thumbImageLink'], si)
			
			if not os.path.isfile(si):
				print "ERROR :: " + str(si) + " was not saved!!"

'''
Get a list of all the titles stored and their id numbers
'''	

#+ ',' + su.encase_in_quotes(str(retailer),'`') 
sql = "SELECT " + su.encase_in_quotes(str(productTitle),'`') + ',' + su.encase_in_quotes(str(productID),'`') + " FROM " + su.encase_in_quotes(str(db),'`') + '.' + su.encase_in_quotes(str(tableName),'`')
cur.execute(sql)
getStoredTitles = cur.fetchall()

#for i in getStoredTitles:
#	print i[0]



'''
Get a list of all the individual page links for each product
'''
sql = "SELECT " + su.encase_in_quotes(str(productID),'`') + ',' + su.encase_in_quotes(str(productPage),'`') + " FROM " + su.encase_in_quotes(str(db),'`') + '.' + su.encase_in_quotes(str(tableName),'`')
cur.execute(sql)
getproductPages = cur.fetchall()

#for i in getproductPages:
#	print i[1]

'''
Loop through the page linkes and:
1. Collect all the information for each product
2. Store the data in the database
3. Save the images associated with the product
'''
#
product_image_link = {}

subPage = requests.get('http://www.sanity.com.au/products/2312575/Last_Kingdom_-_Season_1_The')


#Create a tree of elements from a string containing XML
elementTree = html.fromstring(subPage.content)
print elementTree.tag

for i in elementTree.iterchildren():
	print i
	

product_image_link['productImageLink'] = elementTree.xpath('//div[@id="product-image"]/img/@src')[0]

print product_image_link



#product_image_link['productImageLink'] = elementTree.xpath('//div[@class="mainContent"]/img/@src')

#product_image_link['productImageLink'] = elementTree.xpath('//div[@class="container"]/img/@src')
#print product_image_link['productImageLink']
'''
for g in getproductPages:


	
	#Using xPath Expressions:
	#1. get the href and title attribute values of all anchor tags that are the child of div tags containing the class "thumb-image"
	#2. get the scr value of all image tags that are the child of div tags containing the class "thumb-image"
	product_image_link = {}
	
	print g[1]
	subPage = requests.get('http://www.sanity.com.au/products/2312575/Last_Kingdom_-_Season_1_The')
	product_image_link['productImageLink'] = etree.xpath('//div[@class="mainContent"]')
	print product_image_link['productImageLink']
	
	#Create a tree of elements from a string containing XML
	#etree = html.fromstring(subPage.content)
	
	
	#productPage will get the product page from the "thumb-image" that contains all the data about the product
	#product_image['productImageLink'] = etree.xpath('//div[@class="mainContent"]/img')
	#print product_image['productImageLink']
'''
cur.close()
conn.close()
print "end"

# REFERENCE AND TESTING PURPOSES ONLY FOR SORTING DICTIONARIES 
#print sorted(content.keys())
#for i in sorted(content.keys()):
#	print content.keys()