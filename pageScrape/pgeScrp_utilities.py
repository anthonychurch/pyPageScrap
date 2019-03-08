'''
Check the sizes of the links, title and img len to see if they match
'''
def check_if_list_len_matches(list):
	result = False
	previous = len(list[0])

	for l in list:
		if len(l) == previous:
			print 'length matches'
			result = True
		else:
			print 'length does not match'
			result = False
	return result

'''
Checks the size of the value component of the dictionary items injected in the *argv
In this instance the dictionary structure expected is :- {'key':['value1','value2,'value3','value4']} 
'''
def check_if_dict_value_len_matches(*argv):
	result = False
	previous = len(argv[0].values()[0])

	for arg in argv:
		if len(arg.values()[0]) == previous:
			result = True
		else:
			result = False

	return result

	
def replace_illegal_char(strng,noChars,replChar):	
	for c in noChars:
		for i in range(0,len(strng),1):
			test = strng[i].find(c)
			
			if test != -1:
				replace = replChar + c
				strng[i] = strng[i].replace(c,replace)
	
	return strng
			
'''	
Filters and sort through links, title and img, matching each criteria to each other:
*argv = a nested list of dictionaries whose index values are mapped to each other.
         The aim is to interate through each list and assign each mapped value to a list value, which is mapped to a key
		  EXAMPLE: {'key':['value1','value2,'value3','value4']}
start = is the next unused index number from the table that this data is to be injected into.
prefix = the string prefix for the key string in the output dictionary
padding = this the zero padding for the sufix of the key string
'''
def get_captured_data(start,prefix,padding,*argv):
	# Declare a empty temporary dictionary array to be returned 
	content = {}
	inc = start
	# Set zero padding 
	pad = "%0"+str(padding)+"d"
	
	# Checks to make sure the the length of each listv matches.
	# If they do not match, something has gone wrong with the network connection or the website is missing the appropriate data.
	# Check the website link.
	if check_if_dict_value_len_matches(*argv):
		# REFERENCE : Get the of first dictionary key
		#print argv[0].keys()[0]
		# REFERENCE : Get the len of first dictionary value
		#print len(argv[0].values()[0])
		
		# Loop get the length of one of the nested arrays and use that value for length of the loop
		for i in range (0,len(argv[0].values()[0]),1):
			# Declare the key that the different index values that are to be mapped to
			key = prefix+str(pad % (i))
			#print key
			# Declare a empty temporary dictionary array to store the different index values to be mapped to the key
			temp = {}
	
			# Loop though each arg in argv and map their index values to each other as a nested dictionary array
			for arg in argv:
				'''
				print str(arg.keys()[0])
				print str(arg.values()[0][i])
				print '         '
				'''
				temp[str(arg.keys()[0])] = str(arg.values()[0][i])

			# Append to the return dictionary array	
			content[key] = temp
			#print '          '
			
	else:
		content[False] = {'error' : '*argv dictionary array did not match in length. This means data did not download correctly from the website. Check your internet connection or website'}
		
	return content