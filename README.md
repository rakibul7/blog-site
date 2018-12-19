# Django-Blog

A ready to use blog application to maintain your blog. Use this to maintain your blog in an easy manner and spread your information to world.

#### This application uses Python based Django framework for its backend and SQLite as local database. If you want to switch to another database type, you can do so by changing necessary files before running commands.
___

### Features of This Blog :
- **Admin interface** with all privilages to access modify all posts.
- Admin can **invite** other users to post by registering them as User from **Django-admin panel**. Other users have limited privilages.
- Posts can be saved as **draft** before they can be shared with public.
- Users are not allowed to touch sensitive information without logging in and without having sufficient privilages.

___
To get this blog **running** on your local machine. **Clone** the directory and activate your python **virtual environment**. After you setup your virtual environment. **Run** following commands.

    pip install django
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py makemigrations blog
    python manage.py migrate blog
    python manage.py createsuperuser
    python manage.py runserver
___
## Important!

#### After successfully executing these commands, just go to `localhost:8000` to browse your blog. The following urls and instructions are useful in this blog.

- `localhost:8000/accounts/login` to login with your account. You can use your **admin account** to login with admin privilages.
- `localhost:8000/admin` to access django **admin interface**.
- If in settings.py **DEBUG** mode is set to **false** please run `python manage.py runserver --insecure` to run server and render static files correctly on local testing.
- Admin can login from either from Django admin or blog login page to get logged in.
- Fill out the details like First Name, Last Name etc in the Django-admin Users model to render them in the blog.

Enjoy :+1:

___
![Home Page](1.gif)