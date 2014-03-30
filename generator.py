import sys, yaml

create_table_string = 'CREATE TABLE "{0}" (\n{0}_id serial,'
field_string = '{table_name}_{field_name} {field_type},'
	
update_function_string = """CREATE OR REPLACE FUNCTION {0}_on_update() RETURNS trigger AS ${0}_on_update$
	BEGIN
		NEW.category_updated := current_timestamp;
		RETURN NEW;
	END;
${0}_on_update$ LANGUAGE plpgsql;
"""

update_trigger_string = """CREATE TRIGGER {0}_update_trigger BEFORE UPDATE ON {0}
FOR EACH ROW
EXECUTE PROCEDURE {0}_on_update();
"""

one_to_many_string = """ALTER TABLE "{0}" ADD CONSTRAINT fk_{0}_{1} FOREIGN KEY ({1}_id) REFERENCES "{1}" ({1}_id);
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

def create_table(entities, entity):
	ddl = [create_table_string.format(entity)]
	for key in entities[entity]['fields']:
		ddl.append(field_string.format(table_name = entity, field_name = key, field_type = entities[entity]['fields'][key]))
	ddl.append(timestamp_fields_string.format(entity))
	return '\n'.join(ddl)

def alter_table(entities, entity):
	relation_string = []
	relations = entities[entity]['relations']
	if relations != {}:
		for relation in relations:
			if relation.lower != entity:
				relation_type = relations[relation]
				neighbor = entities.get(relation.lower(), None)
				if neighbor != None:
					neighbor_relations = neighbor['relations']
					if neighbor_relations.get(entity.title(), '') == 'many':
						if relation_type == 'one':
							relation_string.append(one_to_many_string.format(entity, relation.lower()))
						elif relation_type == 'many':
							# import ipdb; ipdb.set_trace();
							neighbor_relations[entity.title()] = 'many_done'
							relation_string.append(many_to_many_string.format(entity, relation.lower()))
	return '\n'.join(relation_string)

def add_triggers(entity):
	return '\n'.join((update_function_string.format(entity), update_trigger_string.format(entity)))

if __name__ == '__main__':
	yaml_file = sys.argv[1]
	entities = {}
	with open (yaml_file, "r") as yaml_file:
		schema = yaml.safe_load(yaml_file)
		for (table_name, elements) in schema.items():
			table_name = table_name.lower()
			entities[table_name] = {'fields':elements.get('fields', {}), 'relations':elements.get('relations', {})}
	queries = []
	
	for entity in entities:
		queries.append(create_table(entities, entity))

	for entity in entities:
		alter_query = alter_table(entities, entity)
		if alter_query != '':
			queries.append(alter_query)
	
	for entity in entities:
		queries.append(add_triggers(entity))
		
	for query in queries:
		print query
