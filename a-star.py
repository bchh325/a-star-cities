import math
import copy
import sys

cities_list = []


map_file = open('map.txt', 'r')
coordinates_file = open('coordinates.txt', 'r')

map = map_file.read().splitlines()
coordinates = coordinates_file.read().splitlines()

class City:
    class ConnectedCity:
        def __init__(self, name: str, dist: float, latitude: float, longitude: float):
            self.name = name
            self.distance = dist
            self.latitude = latitude
            self.longitude = longitude
            self.id = None

        def __str__(self):
            return f"{self.name} | Distance {self.distance} | ({self.latitude}, {self.longitude})"

        def __repr__(self):
            return f"{self.name} | Distance: {self.distance} | ({self.latitude}, {self.longitude})"

    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.connected_cities = []
        self.id = None

    def __str__(self):
        return f"{self.name}: ({self.latitude}, {self.longitude})"

    def __repr__(self):
        return f"{self.name}"

    def addCity(self, name, dist, lat, long):
        city = self.ConnectedCity(name, dist, lat, long)
        self.connected_cities.append(city)

for line in coordinates:
    city_data = line.split(':')
    city_data[1] = city_data[1][1:-1]
    city_data[1] = city_data[1].split(',')

    city_data[1][0] = float(city_data[1][0])
    city_data[1][1] = float(city_data[1][1])

    city = City(city_data[0], city_data[1][0], city_data[1][1])
    cities_list.append(city)

for line in map:
    city_data = line.split('-')
    city_data[1] = city_data[1].split(',')
    for i in range(len(city_data[1])):
        city_data[1][i] = city_data[1][i].replace("(", ":")
        city_data[1][i] = city_data[1][i].replace(")", "")

    for city in cities_list:
        if (city.name == city_data[0]):
            for connectedCity in city_data[1]:
                temp = connectedCity.split(":")
                lat = None
                long = None
                for x in cities_list:
                    if (x.name == temp[0]):
                        lat = x.latitude
                        long = x.longitude
                city.addCity(temp[0], float(temp[1]), lat, long)

for i in range(len(cities_list)):
    cities_list[i].id = i

for i in cities_list:
    for j in i.connected_cities:
        for k in cities_list:
            if j.name == k.name:
                j.id = k.id


def sld(c1: City, c2: City):
    c1_lat = c1.latitude * (math.pi / 180)
    c1_long = c1.longitude * (math.pi / 180)

    c2_lat = c2.latitude * (math.pi / 180)
    c2_long = c2.longitude * (math.pi / 180)

    formula = math.sqrt(((math.sin((c2_lat - c1_lat) / 2)) ** 2) + (
                math.cos(c1_lat) * math.cos(c2_lat) * ((math.sin((c2_long - c1_long) / 2)) ** 2)))

    return 2 * 3958.8 * math.asin(formula)

def algorithm(c1: City, c2: City):
    search_list = []
    finish_list = []

    def checkMin(l):
        temp = []
        for item in l:
            temp.append(item.total)

        return min(temp)

    class CityData:
        def __init__(self, index, prev, name):
            self.index = index
            self.prev = prev
            self.name = name

            self.g = None
            self.h = None

            self.total = None

        def updateG(self, g):
            self.g = g

        def updateH(self, h):
            self.h = h

        def calculateTotal(self):
            self.total = self.g + self.h

        def __str__(self):
            return f"{self.name}"

        def __repr__(self):
            return f"{self.name}"

    data = CityData(c1.id, None, c1.name)
    data.updateG(0)
    data.updateH(sld(c1, c2))
    data.calculateTotal()

    search = []
    finalMin = data.total
    search.append(data)
    looping = True
    cityToReturn = None

    while looping:
        # print()
        min_list = []
        for item in search:
            min_list.append(item.total)

        minTotal = min(min_list)
        currentSearch = search.pop(min_list.index(minTotal))
        for city in copy.deepcopy(cities_list[currentSearch.index].connected_cities):
            data = CityData(city.id, currentSearch, city.name)
            for conCity in copy.deepcopy(cities_list[currentSearch.index].connected_cities):
                if conCity.name == data.name:
                    data.updateG(data.prev.g + conCity.distance)
                    data.updateH(sld(conCity, c2))
                    data.calculateTotal()

            search.append(data)

        temp = []
        for item in search:
            temp.append(item.total)

        for item in search:
            if item.h == 0 and item.total <= min(temp):
                cityToReturn = item
                looping = False

        # print(f"MIN: {min(temp)}")

        #for i in search:
            #print(f"{i.name} = G: {i.g} | H: {i.h} | Total: {i.total}")

        #print()

    return cityToReturn

def formatOutput(city):
    cities = []

    currCity = city
    while not currCity == None:
        cities.append(currCity.name)
        currCity = currCity.prev

    print("Best Route: ", end="")
    for i in range(len(cities) - 1, -1, -1):
        if not i == 0:
            print(cities[i], end=" - ")
        else:
            print(cities[i])

    print(f"Total distance: {city.total:.2f} mi")

def main():
    inputs = sys.argv

    input1 = str(inputs[1]).strip()
    input2 = str(inputs[2]).strip()


    starting = None
    destination = None

    for city in cities_list:
        if (city.name == input1):
            starting = copy.deepcopy(city)
        elif (city.name == input2):
            destination = copy.deepcopy(city)

    finalDestination = algorithm(starting, destination)

    print(f"From city: {input1}")
    print(f"To city: {input2}")
    formatOutput(finalDestination)

if __name__ == "__main__":
    main()




