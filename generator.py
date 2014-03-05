import sys, yaml

class DDLStatement(object):
	def __init__(self, table_name, elements):
		self.table_name = table_name.lower()
		self.fields = elements['fields']

	def __repr__(self):
		return self.__build_statement()

	def __build_statement(self):
		entity = ['CREATE TABLE "{0}" (\n{0}_id serial,'.format(self.table_name)]
		for key in self.fields:
			field_string = '{table_name}_{field_name} {field_type},'
			entity.append(field_string.format(table_name = self.table_name, field_name = key, field_type = self.fields[key]))
		entity.extend(['%s_created timestamp NOT NULL DEFAULT current_timestamp,' % self.table_name,
						'%s_updated timestamp NOT NULL DEFAULT 0,' % self.table_name,
						'PRIMARY KEY (%s_id)' % self.table_name,
						');\n'])
		return '\n'.join(entity)

def generate_statement(from_yaml):
	queries = []
	with open (from_yaml, "r") as yaml_file:
		data = yaml.load(yaml_file)
	for (table_name, elements) in data.items(): 
		queries.append(DDLStatement(table_name, elements))
	return queries

if __name__ == '__main__':
	yaml_file = sys.argv[1]

 	statement = generate_statement(yaml_file)
	print statement;
