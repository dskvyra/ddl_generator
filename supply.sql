
{'Category':
	{'fields': 
		{'title': 'varchar(50)'}
	}, 
'Article':
	{'fields':
		{'text': 'text',
		'title': 'varchar(50)'}
		}
}

CREATE TABLE "category" (
category_id serial,
category_title varchar(50) NOT NULL,
category_created timestamp NOT NULL DEFAULT current_timestamp,
category_updated timestamp DEFAULT NULL,
PRIMARY KEY (category_id)
);

CREATE TABLE "article" (
article_id serial,
article_text text NOT NULL,
article_title varchar(50) NOT NULL,
article_created integer NOT NULL DEFAULT cast(extract(epoch from now()) as integer),
article_updated integer NOT NULL DEFAULT 0,
PRIMARY KEY (article_id)
);


CREATE DATABASE "test";

CREATE TABLE "category" (
category_id serial,
category_title varchar(50) NOT NULL,
category_created timestamp NOT NULL DEFAULT current_timestamp,
category_updated timestamp DEFAULT NULL,
PRIMARY KEY (category_id)
);

CREATE OR REPLACE FUNCTION on_update() RETURNS trigger AS $on_update$
	BEGIN
		NEW.category_updated := current_timestamp;
		RETURN NEW;
	END;
$on_update$ LANGUAGE plpgsql;

CREATE TRIGGER category_update_trigger BEFORE UPDATE ON category
FOR EACH ROW
EXECUTE PROCEDURE on_update();

INSERT INTO "category" (category_title) VALUES ('Hello!');
UPDATE "category" SET category_title = '!olleH' WHERE category_id = 1;
SELECT * FROM category;

DROP FUNCTION on_update() cascade;
DROP TABLE category;
DROP DATABASE test;