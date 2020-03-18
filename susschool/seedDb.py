source myvenv/bin/activate
python manage.py shell
from susschool.models import School
from susschool.models import Area
from susschool.models import Reading

# delete all data
Reading.objects.all().delete()
Area.objects.all().delete()
School.objects.all().delete()

# set up st mary's using default colour
st_marys = School.objects.create(id=1,name='St Mary\'s', code='stm')
st_marys_year_r = Area.objects.create(id=1, school=st_marys, name='year r')
st_marys_year_1 = Area.objects.create(id=2, school=st_marys, name='year 1')
st_marys_year_2 = Area.objects.create(id=3, school=st_marys, name='year 2')
st_marys_year_3 = Area.objects.create(id=4, school=st_marys, name='year 3')
st_marys_year_4 = Area.objects.create(id=5, school=st_marys, name='year 4')
st_marys_year_5 = Area.objects.create(id=6, school=st_marys, name='year 5')
st_marys_year_6 = Area.objects.create(id=7, school=st_marys, name='year 6')
st_marys_hall = Area.objects.create(id=8, school=st_marys, name='hall')
st_marys_playground = Area.objects.create(id=9, school=st_marys, name='playground')
Reading.objects.create(area=st_marys_year_r, type='Bin', amount=7)
Reading.objects.create(area=st_marys_year_3, type='Light', amount=4)
Reading.objects.create(area=st_marys_year_5, type='Bike', amount=11)

#set up another sample school
st_anothers_school = School.objects.create(id=2, name='St Another\'s', code='stan', colour='bg-success')
st_anothers_year_r = Area.objects.create(id=11, school=st_anothers_school, name='year r')
st_anothers_year_1 = Area.objects.create(id=12, school=st_anothers_school, name='year 1')
st_anothers_year_2 = Area.objects.create(id=13, school=st_anothers_school, name='year 2')
st_anothers_year_3 = Area.objects.create(id=14, school=st_anothers_school, name='year 3')
st_anothers_year_4 = Area.objects.create(id=15, school=st_anothers_school, name='year 4')
st_anothers_year_5 = Area.objects.create(id=16, school=st_anothers_school, name='year 5')
st_anothers_year_6 = Area.objects.create(id=17, school=st_anothers_school, name='year 6')
st_anothers_hall = Area.objects.create(id=18, school=st_anothers_school, name='hall')
st_anothers_playground = Area.objects.create(id=19, school=st_anothers_school, name='playground')
Reading.objects.create(area=st_anothers_year_1, type='Bin', amount=2)
Reading.objects.create(area=st_anothers_year_2, type='Light', amount=3)
Reading.objects.create(area=st_anothers_hall, type='Bike', amount=4)



