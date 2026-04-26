import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from django.contrib.auth.models import User

# Replace with the credentials you want
username = 'admin1'
email = 'mhmdabouhamoud@gmail.com'
password = 'Mhmd1245'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser {username} created successfully!")
else:
    print("Superuser already exists.")