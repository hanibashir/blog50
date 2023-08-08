

-- create users table
CREATE TABLE 'users' (
`id` INTEGER NOT NULL,
`first_name` TEXT NOT NULL,
`last_name` TEXT NOT NULL,
`email` TEXT NOT NULL,
`password_hash` TEXT NOT NULL,
'about' TEXT DEFAULT NULL,
PRIMARY KEY (`id`)
);
CREATE INDEX uq_email ON users (email);

-- create posts table
CREATE TABLE posts (
`id` INTEGER NOT NULL PRIMARY KEY,
`author_id` INTEGER NOT NULL,
`category_id` INTEGER NULL DEFAULT 0,
`title` TEXT NOT NULL,
`slug` TEXT NOT NULL,
`published` TINYINT(1) NOT NULL DEFAULT 0,
`created_at` DATETIME NOT NULL,
`content` TEXT NULL DEFAULT NULL,
CONSTRAINT fk_author_id
FOREIGN KEY (author_id)
REFERENCES users (id)
ON DELETE CASCADE
);

CREATE INDEX uq_slug ON posts (slug);

-- create comments table
CREATE TABLE post_comments (
`id` INTEGER NOT NULL,
`post_id` INTEGER NOT NULL,
`title` TEXT NOT NULL,
`published` TINYINT(1) NOT NULL DEFAULT 0,
`createdAt` DATETIME NOT NULL,
`publishedAt` DATETIME NULL DEFAULT NULL,
`content` TEXT NULL DEFAULT NULL,
PRIMARY KEY (`id`),
FOREIGN KEY (`post_id`)
REFERENCES posts (`id`)
);

-- create categories table
CREATE TABLE 'categories' (
`id` INTEGER NOT NULL,
`title` TEXT NOT NULL,
'description' TEXT NULL DEFAULT NULL,
'slug' TEXT DEFAULT NULL,
PRIMARY KEY (`id`));



