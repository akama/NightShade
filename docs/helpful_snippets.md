### Add a new tenent

1. Run `manage.py shell` this will get you to a django shell. 

2. Run the code below in the shell. Be sure to change *schema_name* as it will be what is used for the client in the database. The *name* parameter will be what is displayed on the front page of the CTF site. 

```
from customers.models import Client

tenant = Client(domain_url='subdomain.isusec.com',
                schema_name='client_name',
                name='Client Name')

tenant.save()
```

### Find a existing tenant and change them

1. Run `manage.py shell`. 

2. The following code is an example and should be used for reference. 

```
from customers.models import Client

for e in Client.objects.all():
	print(e.schema_name)
	
a = Client.objects.filter(schema_name='client_name').first()

# make the changes you need here. 

a.save()
```

### Add a new super user. 
 
1. Run `python manage.py tenant_command createsuperuser` 

2. Choose the client/schema that corresponds to which site you want to create the super user on. 

3. Enter a username for the password. 

4. Feel free to put in the email or not, it doesn't currently do anything but it may in the future. 

5. Enter the password twice. 

6. The user is now created. Enjoy.

### How to manage NightShade on AWS Elastic Beanstalk

1. SSH into web tier instance.

2. Run the following commands to get the correct enviroment. 

```
source /opt/python/run/venv/bin/activate
source /opt/python/current/env
cd /opt/python/current/app
```

You can now run normal manage.py commands as you would normally. 

