# resource_booking
# Step 1 :-
# Install all the required packages

pip install -r req.txt

# Step 2:-

Create database in Postgres via PGadmin with user postgres and password as you want and add in settings.py.

# Step 3:-
# To replicate the models in db
1. Verify there is only __init__.py file in migration folder than run the below  command 
2. py manage.py makemigrations 
3. py manage.py migrate 

# Step 4:-
# To run server run the below command:-
py manage.py runserver

# Step 5:-
# To create superuser:-
py manage.py createsuperuser
.Using Admin panel to add resources 

