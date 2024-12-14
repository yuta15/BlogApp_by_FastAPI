CREATE TABLE IF NOT EXISTS main.user(
	`uuid` CHAR(32) NOT NULL, 
	`username` VARCHAR(50) NOT NULL, 
	`email` VARCHAR(255) NOT NULL, 
	`create_at` DATETIME NOT NULL, 
	`update_at` DATETIME NOT NULL, 
	`hashed_password` VARCHAR(255) NOT NULL, 
	`is_active` BOOL NOT NULL, 
	`is_admin` BOOL NOT NULL,
	PRIMARY KEY (uuid)
);
CREATE UNIQUE INDEX ix_user_uuid ON user(uuid);
CREATE UNIQUE INDEX ix_user_username ON user(username);
CREATE UNIQUE INDEX ix_user_email ON user(email);


CREATE TABLE article (
	`id` CHAR(32) NOT NULL, 
	`title` VARCHAR(150) NOT NULL, 
	`body` LONGTEXT, 
	`creaeted_at` DATETIME NOT NULL, 
	`updated_at` DATETIME NOT NULL, 
	`is_public` BOOL NOT NULL, 
	`user_id` CHAR(32) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (uuid)
);
CREATE INDEX ix_article_id ON article(id);
CREATE INDEX ix_article_user_id ON article(user_id);