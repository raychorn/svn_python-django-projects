# define a basic city class
class City:
  name = ""
  country = ""
  elevation = 0 
  population = 0

# create a new instance of the City class and
# define each attribute
city1 = City()
city1.name = "Cusco"
city1.country = "Peru"
city1.elevation = 3399
city1.population = 358052

# create a new instance of the City class and
# define each attribute
city2 = City()
city2.name = "Sofia"
city2.country = "Bulgaria"
city2.elevation = 2290
city2.population = 1241675

# create a new instance of the City class and
# define each attribute
city3 = City()
city3.name = "Seoul"
city3.country = "South Korea"
city3.elevation = 38
city3.population = 9733509

cities = [city1, city2, city3]

def city_picker(__cities__, parms):
  key1, value1, key2 = parms
  c = [city for city in __cities__ if ((key1 in city.__dict__.keys()) and (city.__dict__[key1] >= value1))]
  return sorted(c, key=lambda city:city.__dict__[key2] if (key2 in city.__dict__.keys()) else None)

def max_elevation_city(min_population, the_cities=cities):
  return_city = City()

  new_list = city_picker(the_cities, ("population", min_population, "elevation"))
  if (len(new_list) > 0):
    return_city = new_list[-1]
  return "{}, {}".format(return_city.name, return_city.country) if (len(return_city.name) and len(return_city.country)) else ""


print(max_elevation_city(100000)) # Should print "Cusco, Peru"
print(max_elevation_city(1000000)) # Should print "Sofia, Bulgaria"
print(max_elevation_city(10000000)) # Should print ""