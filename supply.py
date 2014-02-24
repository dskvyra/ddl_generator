
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

	create sequence autoincrement_article_id;
	create table article (
	article_id int primary key default nextval('autoincrement_article_id'),
	article_title varchar(50),
	article_text text
	);

	create sequence autoincrement_category_id;
	create table category (
	category_id int primary key default nextval('autoincrement_category_id'),
	category_title varchar(50)
	);


	article (с полями article_id, article_title, article_text) и category (category_id, category_title). 