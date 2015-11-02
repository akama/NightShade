NightShade is a simple security capture the flag framework that is designed to make running your own contest as easy as possible. 

SCREENSHOTS
-----------

They say a screen shot is worth a thousand words.

A challenge page.
![Challenge](https://github.com/UnrealAkama/NightShade/raw/master/screenshots/challenge.png)

A jeopardy style capture the flag.
![Jeopardy Style CTF](https://github.com/UnrealAkama/NightShade/raw/master/screenshots/jeopardy_style_ctf.png)

A traditional style capture the flag.
![Listing Style CTF](https://github.com/UnrealAkama/NightShade/raw/master/screenshots/listing_style_ctf.png)

A blind style capture the flag.
![Blind Style CTF](https://github.com/UnrealAkama/NightShade/raw/master/screenshots/blind_style_ctf.png)

A user profile.
![User Profile](https://github.com/UnrealAkama/NightShade/raw/master/screenshots/user_profile.png)

A list of all the contests.
![Contest Lists](https://github.com/UnrealAkama/NightShade/raw/master/screenshots/contest_lists.png)


HOSTING/SAAS
------------

If you want someone to host your platform, contact me. If you are a non-profit or a educational group, I might be willing to host it for free.

INSTALLING
----------

Install all the requirements in the requirements.txt

    pip install -r requirements.txt

Now we have to setup the database. This is a bit strange because it is designed to run multiple sites at the same time but this isn't needed for most people.

    python manage.py migrate_schemas --shared
    python manage.py migrate_schemas

Now we have to add the domain we want to use so that django starts serving requests from those domains. This must all be entered in the python shell.

    python manage.py shell

Then change the values and enter the following statements.

    from customers.models import Client

    # create your first real tenant
    tenant = Client(domain_url='your.domain.here.com', # don't add your port or www here or things will break.
                    schema_name='shortname',
                    name='Name of Organization')

    tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!

Note on using manage.py, you will have to prefix commands with 'tenant_command'.

    python manage.py tenant_command createsuperuser

Then you will have to enter the schema you wish to use, which is the shortname/schema_name from above. After that, everything should continue to be normal. 
Speaking of which, you should go ahead and create a superuser using the command above. Then visit your.domain.here.com/admin and get started creating your first contest.

You may now serve NightShade using anyway you would like. Nginx and gunicorn is how I serve it, but other ways should work just as well.

If you run into problems, please report them. This is a new project and things may be horrible wrong. Pull requests are always welcome as well.
