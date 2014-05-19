<h2>How to deploy an already existing Django app to Heroku</h2>
<p><a href="http://topshelf-kitchen.herokuapp.com/">Visit the live page here on Heroku </a>(NOTE: It's still in prototype mode)</p>
<br>

<h3>Getting Started</h3>
<p>These instructions assume that you are running Ubuntu/OS X. </p>
<p><u>Windows users will <strong>NOT</strong> be able to push to Heroku.</u> You will need to setup a <a href="https://www.virtualbox.org/wiki/Downloads">virtual machine</a> that runs Linux, Ubuntu, or OS X. This was helpful with getting your [Ubuntu virtual machine started.](http://funinstall.blogspot.com/2013/07/ubuntu-django-and-heroku.html?m=1)</p>
<br>
<p>Ok, time to go through Heroku's instructions, with my notes. Some are in angry red.</p>
<br>
<p><blockquote style="font-size:16px"><strong>$ mkdir hellodjango && cd hellodjango </strong><br><br>
Make sure you’re using the latest virtualenv release. If you’re using a version that comes with Ubuntu, you may need to add the --no-site-packages flag.</blockquote>
<span style="color:red">If you already have a project or project/app created, you can skip this.</span> 
<br><br><br>
<blockquote style="font-size:16px"><strong>$ virtualenv venv </strong><br></blockquote></p>
<p style="color:red">UBUNTU USERS, DO THIS INSTEAD: **$ virtualenv venv --no-site-packages**</p>
<p>I completely skipped over the part above where they talked about --no-site-packages.<br>
Heroku didn't explain the reason for it. It's important! It stops your desktop's applications from loading up in your virtualenv. </p>

<p style="color:red"> It will keep your requirements.txt file clean. Heroku will try to load everything that goes into requirements.txt and will throw errors because it's loading things that are Ubuntu-only. 
</p> 
<br>
<p><blockquote style="font-size:16px"><strong>$ source venv/bin/activate</strong><br></blockquote></p>
<p>Run this every time you edit your project. **The virtualenv can be stored in your project's root.**</p>
<br>
<p><blockquote style="font-size:16px"><strong>$ pip install django-toolbelt</strong><br></blockquote></p>
<p>This is fine. <strong>You may also need to install other packages into your virtualenv that your project uses (South, etc.).</strong></p>
<br>
<p><blockquote style="font-size:16px"><strong>$ django-admin.py startproject hellodjango .</strong><br></blockquote></p>
<p>Start your project if you're not deploying an existing project.</p>
<br>
<p><blockquote style="font-size:16px"><strong>web: gunicorn hellodjango.wsgi</strong><br></blockquote></p>
<p style="color:red">First, create a Procfile at your project root, where manage.py is. Do <strong>touch Procfile</strong>, then edit that file in a text editor. **DO NOT CREATE PROCFILE.txt.**</p>

<p>Heroku assumes that you know what a Procfile is. Heroku called it a text file, which is really confusing to first-time users. Procfile is a standalone file which you can edit in any text editor.</p>

<p>Heroku needs to run 0.0.0.0:8000 so try not to change the default-- you may end up just changing it back later.</p>

<p><a href="http://stackoverflow.com/questions/18374878/gunicorn-on-heroku-binding-to-localhost">Here's how to change the default</a>, but it's best to avoid changing it.</p>
<br>
<br>
<p><strong>What heroku totally forgot to address: your database. </strong>This was the biggest headache of all. If you're running Postgres, great. You'll have fewer problems. Make sure to sync and do schemamigrations before moving forward.</p>

<p><strong>If you're running another database, you'll need to convert it to Postgres.</strong> There are three options:
<ul>
<li><a href="https://devcenter.heroku.com/articles/heroku-mysql">Convert from MySQL to Postgres using a Ruby gem</a></li>
<li><a href="http://stackoverflow.com/questions/3807324/migrating-data-to-postgres-from-mysql-with-django-how-do-i-migrate-generic-tab">Dump your data and load it into Postgres</a> (This can be buggy. Make sure to preserve your original database until you're sure it's working.)</li>
<li>Import your data using a custom manage.py command.</li>
</ul>
<p>I chose #3. I had scraped a lot of data from external sources and just created another Postgres database, synched my models to it, imported the data with manage.py, and then did a schemamigration. It's not the best one to use if you have a lot of data in your existing database. 
</p>
<p>Converting the database was the most difficult part. Make sure to get this working before you move forward. </p>
<br>
<p><blockquote style="font-size:16px"><strong>$ foreman start</strong><br></blockquote></p>
<p style="color:red">Test out your app here. Should run ok if you've done the above steps properly.</p>
<br>
<p><blockquote style="font-size:16px"><strong>$ pip freeze > requirements.txt</strong><br></blockquote></p>
<p style="color:red">Requirements.txt should be at your project's root level, with manage.py and Procfile. Check the file to make sure the following are installed (versions will change): 
<ul>
<li>Django==1.6</li>
<li>dj-database-url==0.2.2</li>
<li>dj-static==0.0.5</li>
<li>gunicorn==18.0</li>
<li>psycopg2==2.5.1</li>
<li>static==0.4</li>
<li>wsgiref==0.1.2</li>
</ul>


<p>You may also need to add some other packages manually to avoid errors when pushing to heroku. I had to add a <a href="http://docs.python-requests.org/en/latest/user/install/">Requests package </a>into the file, because my views.py used it. </p>
<br>
<p>Add to the bottom of settings.py: <br><blockquote style="font-size:16px">
<strong># Parse database configuration from $DATABASE_URL <br>
import dj_database_url <br>
DATABASES['default'] =  dj_database_url.config()<br>
<br>
# Honor the 'X-Forwarded-Proto' header for request.is_secure()<br>
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')<br>
<br>
# Allow all host headers<br>
ALLOWED_HOSTS = ['*']<br>
<br>
# Static asset configuration <br>
import os <br>
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) <br>
STATIC_ROOT = 'staticfiles' <br>
STATIC_URL = '/static/'<br>

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)</strong><br></blockquote></p>

<p style="color:red">NOPE. This didn't work. <br><br>Replace their database setting with: <strong>DATABASES = {'default':dj_database_url.config(default='postgres://localhost')}</strong><a href="http://stackoverflow.com/questions/11071579/heroku-database-settings-injection-how-do-i-setup-my-dev-django-database">  <br><br>Here's why.</a></p>

<p>You need to do more to get this to work. You may already have some other settings. Get rid of any of the same settings taht Heroku wants to use (BASE_DIR, DATABASES, and ALLOWED HOSTS are loaded by default when you create a project). Get rid of your Postgres database settings completely!<br><br><strong style="color:red">Make sure to add Heroku's settings to the bottom of settings.py.</strong></p>
<br>
<p>Wsgi.py:<br><blockquote style="font-size:16px"><strong>from django.core.wsgi import get_wsgi_application<br>
from dj_static import Cling<br>
<br>
application = Cling(get_wsgi_application())</strong><br></blockquote></p>
<p style="color:red">Replace your entire wsgi file with this. Don't just add it to the end of what you have already.</p>
<br>
<p>Create a .gitignore file and add:<br> <blockquote style="font-size:16px"><strong>
venv
*.pyc
staticfiles</strong><br></blockquote></p>
<p style="color:red">This should also be at your project's root, with manage.py, etc. Like Procfile, .gitignore is a standalone file.</p>
<br>
<p>Git and Heroku launch:<br> <blockquote style="font-size:16px"><strong>
$ git init<br>
$ git add .<br>
$ git commit -m "my django app" <br>
$ heroku create <br>
$ git push heroku master <br>
</strong><br></blockquote></p>
<p style="color:red">If you run into some problems here, just debug one by one. <a href="https://devcenter.heroku.com/articles/keys">You may need to add a SSH key to Heroku before deploying.</a></p>

<p>Test out your app in Heroku. Heroku makes it seem like you're done here. <strong>You're not done!!! You still need to migrate over your database, if you have one.</strong> Instructions are buried after crap about dynos and logs.</p>
<br>
<p>To sync your database with Heroku: <br><blockquote style="font-size:16px"><strong>$ heroku run python manage.py syncdb</strong><br></blockquote></p>
<p style="color:red">You may also need to do <strong>heroku run python manage.py migrate {yourapp}</strong></p>

<p>You can also run shell commands in Heroku with <strong>heroku run python manage.py shell</strong>, which may be helpful for synching and loading data.</p>

<h3>Good luck!!</h3>










