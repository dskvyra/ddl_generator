import sys, yaml, ipdb

class DDLStatement(object):
	def __init__(self, table_name, elements):
		self.table_name = table_name
		self.fields = elements['fields']

	def __repr__(self):
		return self.__build_statement()

	def __build_statement(self):
		table_name_lower = self.table_name.lower()
		create_table_string = 'CREATE TABLE {table_name}(\n{table_name}_id serial primary key'
		fields = [create_table_string.format(table_name = table_name_lower)]
		for key in self.fields:
			field_string = '{table_name}_{field_name} {field_type}'
			fields.append(field_string.format(table_name = table_name_lower, field_name = key, field_type = self.fields[key]))
		# ipdb.set_trace()
		return ',\n'.join(fields) + ');\n'

def generate_statement(from_yaml):
	data = ''
	qrs = []
	with open (from_yaml, "r") as yaml_file:
		data = yaml.load(yaml_file)
	for (table_name, elements) in data.items(): 
		qrs.append(DDLStatement(table_name, elements))
	# ipdb.set_trace()
	return qrs

if __name__ == '__main__':
	yaml_file = sys.argv[1]
	# yaml_file = 'D:\dropbox\Dropbox\Devclub\Junior\Databases\generator\y.yaml'

 	statement = generate_statement(yaml_file)
	print statement;