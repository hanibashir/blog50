
# Blog50 | CS50x Final Project

#### Video Demo: <https://youtu.be/FRiOKu7olwM>
<iframe width="560" height="315" src="https://www.youtube.com/embed/FRiOKu7olwM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

# Final-Project

Blog50 is a web app built with flask to submit as cs50x final project.

#### Description:
My final project in CS50 is a blog with a dashboard. Users must register or login to add posts, categories and comments. Each user has their own control panel where they can control their posts and profiles.

#### Features
* Add posts and categories.

* User's Profile.

* Login and Register.

* Author Page to view all posts by that author.

* Category Page to view all posts in specific category.



#### Directories and Files:



-  `project` - Main Directory.

	-  `db` - contains sql tables script file.

		-  `project_db_script.sql` - sql tables script file.

	-  `falsk_session` - contains session generated files.

	-  `static` - Holds all static files.

		-  `images` - Holds all static images and icons.

			-  `posts` - Holds all posts images.

			-  `users` - Holds all users images.

			-  `user-blue-thumbnail.png` - user default image.

		-  `favicon.ico` - Blog favorite icon.

		-  `styles.css` - Css file.

	-  `templates` - Holds all html files.

		-  `layout.html` - Blog template.

		-  `index.html` - Blog main page.

		-  `apology.html` - Errors messages template.

		-  `category.html` - Show posts in specific category.

		-  `post.html` - Show specific post.

		-  `dashboard` - Contains all dashboard html files.

			-  `layout.html` - Dashboard template.

			-  `index.html` - Dashboard main page.

			-  `new_post.html` - Add new post.

			-  `edit_post.html` - Edit post.

			-  `new_cat.html` - Add new category.

			-  `edit_cat.html` - Edit category.

		-  `user` - Contains all user html files.

			-  `login.html` - Login page.

			-  `register.html` - Register page.

			-  `profile.html` - Register page.

	-  `views` - Contains all routes files.

		-  `blog.py` - Control blog routes.

		-  `dashboard.py` - Control dashboard routes.

		-  `user.py` - Control user routes.

	-  `app.py` - app main file.

	-  `db.py` - all db queries.

	-  `helpers.py` - helper functions.

	-  `project.db` - The blog database.

	-  `requirements.txt` - Project required dependencies.




## How to run the application

* Install project dependencies by running `pip install -r requirements.txt`

* Run `flask run` and visit the link that appears on the command line.