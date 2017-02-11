# Slim blog

A small blog web application writen in Flask. It's goal is to be
as simple and straight forward as possible to setup and use.

It is tailored towards single user blogs only. Although it's possible to
create multiple users. It should be noted that each user can edit *every*
post. If people are reading a posts they don't know who created or
edited the post, you could add a note at the bottom of your posts
who created it of course i.e. *- John*.

## Features

**Implemented:**

* Adding new posts
* Update existing posts
* Markdown previewer when adding or updating posts
* Date and time when the post was created or last edited
* Adding/updating images
* Deleting posts
* Deleting users

**Not yet implemented:**

* A customisable About me page

## Installation (for demo purposes)

*The `$` is used to denote the terminal*

1. Clone the repo with `$ git clone https://github.com/j0holo/slim-blog.git`

2. cd into the project `$ cd /slim-blog`

3. If you want a virtual environment create it with `$ python3 -m venv [name_of_virtualenv]`

    a. If you create a virtual environment switch to it with `$ source [name_of_virtualenv]/bin/activate`
    
    b. Return to your normal python interpreter type `$ deactivate` if your done with running the demo

5. Install the necessary libraries with `$ pip install -r requirements.txt`

6. Run `$ python setup_server.py database --create` to create a new database

7. If you want to view the site with demo data execute `$ python setup_server.py database --populate`.
    **WARNING:** The `--populate` option will add two posts and a user. Don't use this in production.
    You can use this user for testing. See app/models.py:populate_tables()

8. Create a new user with `$ python setup_server.py new_user`

9. Go to the app directory `$ cd app` and start the demo server with `$ python app.py`

10. Enter [127.0.0.1:5000](127.0.0.1:5000) in your browser to view the site

## Setup_server.py commands

TODO: talk about the options/commands the setup_server.py has 

## Issues

In opera 12.10 (Ubuntu 16.04) the `Ctrl + Space` is a shortcut for the
homepage this conflicts with shortcuts.js which uses `Ctrl + Space` to
insert four spaces in the editor. To dissable this in Opera go to
Settings -> Preferences -> Advanced -> Keyboard setup -> "your selected setup"
and search for "Homepage" it will show you a couple of shortcuts to the
homepage. Delete the `Ctrl + Space` shortcut to remove the shortcut.

As of version 12.16 (Ubuntu 16.04) Opera inserts 8 spaces instead of 4.
So currently Opera is not working as intended with the shortcut.js.

## Contribute

If you want to contribute to the project or have an issue, please create a
new issue. In the issue explain what the issue is or what kind of changes
you have in mind.

## License

This project is licensed under the BSD license.