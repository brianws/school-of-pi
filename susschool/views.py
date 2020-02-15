from django.shortcuts import render
from .models import School, Area, Reading
from django.db.models import Sum
import decimal

# Create your views here.
# Reading types
# These values must be the same as the value
# in the model Reading.type.
light_key = 'light'
bin_key = 'bin'
bike_key = 'bike'
    
def areas(request, pk):
    # pk is the school id, and is used to return the areas of the school
    # Assuming all Schools have the same Areas.
    # todo: Would be better if the Areas are dynamic.
    # This means that these hard coded values must have 
    # the same value as Area.name from the models.
    # so far doesn't distinquish between schools, so can only have one school
    year_R_area = "year r"
    year_1_area = "year 1"
    year_2_area = "year 2"
    year_3_area = "year 3"
    year_4_area = "year 4"
    year_5_area = "year 5"
    year_6_area = "year 6"
    hall_area = "hall"
    playground_area = "playground"
    
    # Actual reading from querying the repository
    readings = Reading.objects.filter(area__school__pk = pk)
    year_R_light_readings = get_reading(year_R_area, light_key, readings)
    year_R_bin_readings = get_reading(year_R_area, bin_key, readings)
    year_R_bike_readings = get_reading(year_R_area, bike_key, readings)
    year_1_light_readings = get_reading(year_1_area, light_key, readings)
    year_1_bin_readings = get_reading(year_1_area, bin_key, readings)
    year_1_bike_readings = get_reading(year_1_area, bike_key, readings)
    year_2_light_readings = get_reading(year_2_area, light_key, readings)
    year_2_bin_readings = get_reading(year_2_area, bin_key, readings)
    year_2_bike_readings = get_reading(year_2_area, bike_key, readings)
    year_3_light_readings = get_reading(year_3_area, light_key, readings)
    year_3_bin_readings = get_reading(year_3_area, bin_key, readings)
    year_3_bike_readings = get_reading(year_3_area, bike_key, readings)
    year_4_light_readings = get_reading(year_4_area, light_key, readings)
    year_4_bin_readings = get_reading(year_4_area, bin_key, readings)
    year_4_bike_readings = get_reading(year_4_area, bike_key, readings)
    year_5_light_readings = get_reading(year_5_area, light_key, readings)
    year_5_bin_readings = get_reading(year_5_area, bin_key, readings)
    year_5_bike_readings = get_reading(year_5_area, bike_key, readings)
    year_6_light_readings = get_reading(year_6_area, light_key, readings)
    year_6_bin_readings = get_reading(year_6_area, bin_key, readings)
    year_6_bike_readings = get_reading(year_6_area, bike_key, readings)
    hall_light_readings = get_reading(hall_area, light_key, readings)
    hall_bin_readings = get_reading(hall_area, bin_key, readings)
    hall_bike_readings = get_reading(hall_area, bike_key, readings)
    playground_light_readings = get_reading(playground_area, light_key, readings)
    playground_bin_readings = get_reading(playground_area, bin_key, readings)
    playground_bike_readings = get_reading(playground_area, bike_key, readings)
    
    context = {
        'year_R_light_readings' : year_R_light_readings,
        'year_R_bin_readings' : year_R_bin_readings,
        'year_R_bike_readings' : year_R_bike_readings,
        'year_1_light_readings' : year_1_light_readings,
        'year_1_bin_readings' : year_1_bin_readings,
        'year_1_bike_readings' : year_1_bike_readings,
        'year_2_light_readings' : year_2_light_readings,
        'year_2_bin_readings' : year_2_bin_readings,
        'year_2_bike_readings' : year_2_bike_readings,
        'year_3_light_readings' : year_3_light_readings,
        'year_3_bin_readings' : year_3_bin_readings,
        'year_3_bike_readings' : year_3_bike_readings,
        'year_4_light_readings' : year_4_light_readings,
        'year_4_bin_readings' : year_4_bin_readings,
        'year_4_bike_readings' : year_4_bike_readings,
        'year_5_light_readings' : year_5_light_readings,
        'year_5_bin_readings' : year_5_bin_readings,
        'year_5_bike_readings' : year_5_bike_readings,
        'year_6_light_readings' : year_6_light_readings,
        'year_6_bin_readings' : year_6_bin_readings,
        'year_6_bike_readings' : year_6_bike_readings,
        'hall_light_readings' : hall_light_readings,
        'hall_bin_readings' : hall_bin_readings,
        'hall_bike_readings' : hall_bike_readings,
        'playground_light_readings' : playground_light_readings,
        'playground_bin_readings' : playground_bin_readings,
        'playground_bike_readings' : playground_bike_readings
        }
    return render(request, 'susschool/areas.html', context)

def areas_todo(request, pk):
    # todo: dynamic areas
    areas = Area.objects.filter(school__pk=1)
    
    context = {'areas' : areas}
    
    return render(request, 'susschool/areas_todo.html', context)

def schools(request):
    schools = School.objects.all()
    context = {'schools' : schools}
    
    return render(request, 'susschool/schools.html', context)

def score(request, pk):
    school = School.objects.get(id = pk)
    # areas = Area.objects.filter(school__pk=1)
    readings = Reading.objects.filter(area__school__pk = pk)
    readings_grouped = readings.values('type').annotate(amount=Sum('amount'))
    light_score = get_type_amount(light_key, readings_grouped.filter(type__iexact=light_key))
    bike_score = get_type_amount(bike_key, readings_grouped.filter(type__iexact=bike_key))
    bin_score= get_type_amount(bin_key, readings_grouped.filter(type__iexact=bin_key))
    score = get_sustainable_score(light_score, bike_score, bin_score)
    image_number = get_image_number(score)
    image_name = "{0}.jpg".format(image_number)
    
    context = {'score' : score,
               'image_name' : image_name,
               'school_name' : school.name
              }
    
    return render(request, 'susschool/score.html', context)

def get_reading_old(area_name, reading_type):
    # todo: expensive, hitting db everytime
    reading = Reading.objects.filter(area__name__iexact=area_name).filter(type__iexact=reading_type).aggregate(Sum('amount'))
    reading_value = reading['amount__sum']

    return reading_value

def get_reading(area_name, reading_type, readings):
    # todo: expensive, hitting db everytime?
    reading = readings.filter(area__name__iexact=area_name).filter(type__iexact=reading_type).aggregate(Sum('amount'))
    reading_value = reading['amount__sum']

    return reading_value

def get_type_amount(type_key, query):
    score = 0
    
    if query: # exist?
        score = query.first()['amount']

    return score

def get_sustainable_score(light_score, bike_score, bin_score):
    score = (bike_score  + bin_score) -  light_score
    
    return score

def get_image_number(score):
    if score <= 0:
        return 0
    
    if score >= 100:
        return 100
    
    return round(score, -1)
    

