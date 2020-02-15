# school-of-pi
st mary's school of pi 

This website was developed using the guidlines from the excellent https://tutorial.djangogirls.org/en/ tutorial, 
so it might be prudent to read through this first.
Once the code is downloaded, to launch the web server, do the following in a teminal window:
cd [folder_where_code_is]
source myvenv/bin/activate
python manage.py runserver

You will need to set up the local sqllite database. This can be done (i think) with the following in a terminal window:
cd [folder_where_code_is]
source myvenv/bin/activate
python manage.py makemigrations susschool
python manage.py migrate susschool
# todo: I will provide a script to set up some test data

You should be able to go to the default django admin site (http://127.0.0.1:8000/admin/) to add schools, areas of schools, and readings 
(you might need to set yourself up as an admin first see here: https://tutorial.djangogirls.org/en/django_admin/). 
Please note that in this first draft of the code, there needs to be a set number of "areas" within your school with specific names. 
These are "Year R", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6", "Hall", "Playground" 
(Please note that this will change soon to be dynamic.)
There also needs to be readings of the following types "Bin", "Light", "Bike". 
Once you have added a school in the admin area (http://127.0.0.1:8000/admin/susschool/school/), you should be able to view the school of pi website here:
http://127.0.0.1:8000/schoolofpi/schools/
