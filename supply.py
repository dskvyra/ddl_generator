
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

	print "Hello"

	CREATE TABLE "category" (
	category_id serial,
	category_title varchar(50) NOT NULL,
	PRIMARY KEY "category_id"
	);

	CREATE TABLE "article" (
	article_id serial,
	article_text text NOT NULL,
	article_title varchar(50) NOT NULL,
	PRIMARY KEY "article_id"
	);
