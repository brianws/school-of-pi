cd stmarysschool
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
stmarysschool = School.objects.create(name='St Mary\'s', code='stm')
stanotherschool = School.objects.create(name='St Another\'s', code='stm', )


