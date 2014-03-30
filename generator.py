import sys, yaml

create_table_string = 'CREATE TABLE "{0}" (\n{0}_id serial,'
field_string = '{}_{} {},'
	
update_trigger_string = """CREATE OR REPLACE FUNCTION {0}_on_update() RETURNS trigger AS ${0}_on_update$
	BEGIN
		NEW.category_updated := current_timestamp;
		RETURN NEW;
	END;
${0}_on_update$ LANGUAGE plpgsql;

CREATE TRIGGER {0}_update_trigger BEFORE UPDATE ON {0}
FOR EACH ROW
EXECUTE PROCEDURE {0}_on_update();
"""

one_to_many_string = """ALTER TABLE "{0}" ADD COLUMN {1}_id integer NOT NULL;
ALTER TABLE "{0}" ADD CONSTRAINT fk_{0}_{1} FOREIGN KEY ({1}_id) REFERENCES "{1}" ({1}_id);
"""

many_to_many_string = """CREATE TABLE {0}_{1}(
{0}_id integer REFERENCES {0} ({0}_id) ON UPDATE CASCADE ON DELETE CASCADE,
{1}_id integer REFERENCES {1} ({1}_id) ON UPDATE CASCADE,
CONSTRAINT {0}_{1}_pkey PRIMARY KEY ({0}_id,{1}_id)
);
"""

timestamp_fields_string = """{0}_created timestamp NOT NULL DEFAULT current_timestamp,
{0}_updated timestamp DEFAULT NULL,
PRIMARY KEY ({0}_id)
);
"""

class Generator(object):
	def __init__(self):
		self.entities = {}
		self.queries = []
		self._statment = ''

	def build_ddl(self, schema_file):
		with open (schema_file, "r") as yaml_file:
			schema = yaml.safe_load(yaml_file)
			for (table_name, elements) in schema.items():
				table_name = table_name.lower()
				self.entities[table_name] = {'fields':elements.get('fields', {}), 'relations':elements.get('relations', {})}
			self._statment = self._create_table()

	def dump(self, file_name):
		with open(file_name, "w") as text_file:
			text_file.write(self._statment)

	@property
	def statement(self):
		return self._statment

	def __repr__(self):
		return self.statement

	def clear(self):
		self.entities = {}
		self.queries = []
		self._statment = ''

	def _create_table(self):
		queries = []

		for entity_name in self.entities:
			ddl = [create_table_string.format(entity_name)]
			for key in self.entities[entity_name]['fields']:
				ddl.append(field_string.format(entity_name, key, self.entities[entity_name]['fields'][key]))
			ddl.append(timestamp_fields_string.format(entity_name))
			ddl.append(self._build_triggers(entity_name))
			relations = self._build_relations(entity_name)
			if relations:
				ddl.append(relations)
			queries.append('\n'.join(ddl))
		return '\n'.join(queries)

	def _build_relations(self, entity_name):
		relations = self.entities[entity_name]['relations']
		relation_list = []

		for relation in relations:
			relation_type = relations[relation]
			neighbor = self.entities.get(relation.lower(), None)
			if relation.lower() != entity_name and neighbor['relations'].get(entity_name.title(), '') == 'many':
				if relation_type == 'one':
					relation_list.append(one_to_many_string.format(entity_name, relation.lower()))
				elif relation_type == 'many':
					neighbor['relations'][entity_name.title()] = 'many_done'
					relation_list.append(many_to_many_string.format(entity_name, relation.lower()))
		return '\n'.join(relation_list)

	def _build_triggers(self, entity_name):
		return update_trigger_string.format(entity_name)

if __name__ == '__main__':
	g = Generator()
	g.build_ddl('y.yaml')
	g.dump('statement.sql')
	print g
	g.clear()
