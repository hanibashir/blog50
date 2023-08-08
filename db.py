from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


# db select queuries
def select(table="posts", **kwargs):
    # select from posts
    if table == "posts":
        if "user_id" in kwargs and "post_id" not in kwargs:
            return db.execute(
                "SELECT P.id as post_id, P.title, P.published, P.created_at, P.content, P.slug as post_slug, P.img_url as thumbnail, "
                + "C.id as cat_id, C.title as category, C.description as cat_desc "
                + "FROM posts P JOIN categories C ON P.category_id = C.id WHERE author_id = ? ORDER BY P.id DESC",
                kwargs["user_id"],
            )
        # if the category is deleted
        elif "no_cat" in kwargs and "post_id" in kwargs and "user_id" in kwargs:
            return db.execute(
                "SELECT * FROM posts WHERE author_id = ? AND id = ? ORDER BY id DESC",
                kwargs["user_id"],
                kwargs["post_id"],
            )
        elif "user_id" in kwargs and "post_id" in kwargs:
            return db.execute(
                "SELECT P.id as post_id, P.title, P.published, P.created_at, P.content, P.img_url as thumbnail, "
                + "C.id as cat_id, C.title as category, C.description as cat_desc "
                + "FROM posts P JOIN categories C ON P.category_id = C.id WHERE P.author_id = ? AND P.id = ? ORDER BY P.id DESC "
                + "LIMIT 1",
                kwargs["user_id"],
                kwargs["post_id"],
            )

        elif "post_id" in kwargs and "user_id" not in kwargs:
            return db.execute(
                "SELECT P.id as post_id, P.title, P.published, P.created_at, P.content, P.img_url as thumbnail, P.author_id, "
                + "C.id as cat_id, C.title as category, C.description as cat_desc "
                + "FROM posts P JOIN categories C ON P.category_id = C.id WHERE P.id = ? ORDER BY P.id DESC "
                + "LIMIT 1",
                kwargs["post_id"],
            )
        elif "cat_id" in kwargs:
            return db.execute(
                "SELECT * FROM posts WHERE category_id = ? ORDER BY id DESC",
                kwargs["cat_id"],
            )
        elif "no_cat" in kwargs:
            return db.execute(
                "SELECT * FROM posts WHERE category_id = ? AND author_id = ? ORDER BY id DESC LIMIT 1",
                kwargs["cat_id"],
                session["user_id"],
            )
        elif "limit" in kwargs:
            return db.execute(
                "SELECT * FROM posts ORDER BY id DESC LIMIT ?", kwargs["limit"]
            )
        # elif "current_post" in kwargs "limit" in kwargs:
        #     return db.execute("SELECT * FROM posts ORDER BY id DESC LIMIT ?", kwargs["limit"])
        else:
            return db.execute(
                "SELECT P.id as post_id, P.title, P.published, P.created_at, P.content, P.slug as post_slug, P.img_url as thumbnail, "
                + "C.id as cat_id, C.title as category, C.description as cat_desc, C.slug as cat_slug "
                + "FROM posts P JOIN categories C ON P.category_id = C.id ORDER BY post_id DESC"
            )
    # select from categories
    elif table == "cats":
        if "limit" in kwargs:
            return db.execute(
                "SELECT * FROM categories ORDER BY id DESC LIMIT ?", kwargs["limit"]
            )
        elif "title" in kwargs:
            return db.execute(
                "SELECT * FROM categories WHERE title = ?", kwargs["title"]
            )
        elif "cat_id" in kwargs:
            return db.execute(
                "SELECT * FROM categories WHERE id = ? ", kwargs["cat_id"]
            )
        else:
            return db.execute("SELECT * FROM categories ORDER BY id DESC")
    # select from users
    elif table == "users":
        if "user_id" in kwargs:
            return db.execute("SELECT * FROM users WHERE id = ?", kwargs["user_id"])
    elif table == "comments":
        return db.execute(
            "SELECT * FROM comments CO "
            + "JOIN users U ON CO.user_id = U.id "
            + "WHERE CO.post_id = ? ORDER BY id DESC",
            kwargs["post_id"],
        )


# db insert queries
def insert(table="posts", **kwargs):
    if table == "posts":
        return db.execute(
            "INSERT INTO posts (author_id, category_id, title, slug, published, created_at, content, img_url) VALUES (?,?,?,?,?,?,?,?)",
            kwargs["user_id"],
            kwargs["cat_id"],
            kwargs["title"],
            kwargs["slug"],
            kwargs["status"],
            kwargs["created_at"],
            kwargs["content"],
            kwargs["img_url"],
        )
    elif table == "cats":
        return db.execute(
            "INSERT INTO categories (title, description, slug) VALUES (?,?,?)",
            kwargs["cat_title"],
            kwargs["cat_desc"],
            kwargs["slug"],
        )
    elif table == "users":
        return db.execute(
            "INSERT INTO users (first_name, last_name, email, password_hash, img_url) VALUES (?,?,?,?,?)",
            kwargs["first_name"],
            kwargs["last_name"],
            kwargs["email"],
            kwargs["pwHash"],
            kwargs["img_short_url"],
        )
    elif table == "comments":
        return db.execute(
            "INSERT INTO comments (post_id, user_id, text, published, createdAt) "
            + "VALUES (?,?,?,?,?)",
            kwargs["post_id"],
            kwargs["user_id"],
            kwargs["text"],
            kwargs["published"],
            kwargs["createdAt"],
        )


# db update queries
def update(table="posts", **kwargs):
    if table == "posts":
        if "cat_deleted" in kwargs:
            return db.execute(
                "UPDATE posts SET category_id = ? " + "WHERE author_id = ? AND id = ?",
                kwargs["cat_id"],
                kwargs["user_id"],
                kwargs["post_id"],
            )
        elif "change_img" in kwargs:
            return db.execute(
                "UPDATE posts SET title = ?, slug = ?, published = ?, content = ?, category_id = ?, img_url = ? "
                + "WHERE author_id = ? AND id = ?",
                kwargs["title"],
                kwargs["slug"],
                kwargs["status"],
                kwargs["content"],
                kwargs["cat_id"],
                kwargs["img_short_url"],
                kwargs["user_id"],
                kwargs["post_id"],
            )
        else:
            return db.execute(
                "UPDATE posts SET title = ?, slug = ?, published = ?, content = ?, category_id = ? "
                + "WHERE author_id = ? AND id = ?",
                kwargs["title"],
                kwargs["slug"],
                kwargs["status"],
                kwargs["content"],
                kwargs["cat_id"],
                kwargs["user_id"],
                kwargs["post_id"],
            )
    elif table == "users":
        if "password_hash" in kwargs and "change_img" in kwargs:
            return db.execute(
                "UPDATE users SET first_name = ?, last_name = ?, password_hash = ?, about = ?, img_url = ? WHERE id = ?",
                kwargs["first_name"],
                kwargs["last_name"],
                kwargs["pwHash"],
                kwargs["about"],
                kwargs["img_short_url"],
                kwargs["user_id"],
            )
        elif "password_hash" in kwargs:
            return db.execute(
                "UPDATE users SET first_name = ?, last_name = ?, password_hash = ?, about = ? WHERE id = ?",
                kwargs["first_name"],
                kwargs["last_name"],
                kwargs["pwHash"],
                kwargs["about"],
                kwargs["user_id"],
            )
        elif "change_img" in kwargs:
            return db.execute(
                "UPDATE users SET first_name = ?, last_name = ?, about = ?, img_url = ? WHERE id = ?",
                kwargs["first_name"],
                kwargs["last_name"],
                kwargs["about"],
                kwargs["img_short_url"],
                kwargs["user_id"],
            )
        else:
            return db.execute(
                "UPDATE users SET first_name = ?, last_name = ?, about = ? WHERE id = ?",
                kwargs["first_name"],
                kwargs["last_name"],
                kwargs["about"],
                kwargs["user_id"],
            )
    elif table == "cats":
        return db.execute(
            "UPDATE categories SET title = ?, description = ?, slug = ? WHERE id = ?",
            kwargs["cat_title"],
            kwargs["cat_desc"],
            kwargs["slug"],
            kwargs["cat_id"],
        )


# db delete queries
def delete(table="posts", **kwargs):
    if table == "posts":
        db.execute("DELETE FROM posts WHERE id = ?", kwargs["post_id"])
    elif table == "cats":
        db.execute("DELETE FROM categories WHERE id = ?", kwargs["cat_id"])
