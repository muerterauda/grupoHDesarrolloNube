INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'users', 'users', 2, 'CREATE TABLE users
(
	id INTEGER
		constraint users_pk
			primary key,
	email TEXT not null,
	name TEXT not null,
	avatar text,
	tokens TEXT,
	created_at BLOB
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('index', 'users_email_uindex', 'users', 3, 'CREATE UNIQUE INDEX users_email_uindex
	on users (email)');