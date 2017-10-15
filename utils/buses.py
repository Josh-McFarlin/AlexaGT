import requests
from config import GMaps_key
from utils.bus_stops import routes
from datetime import date


class User:
    lat = 0
    lng = 0

    def __init__(self, address):
        self.address = address
        self.find_coordinates()

    def find_coordinates(self):
        r = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={key}".format(addr=self.address,
                                                                                                key=GMaps_key))
        j = r.json()
        self.lat = j["results"][0]["geometry"]["location"]["lat"]
        self.lng = j["results"][0]["geometry"]["location"]["lng"]

    def __str__(self):
        return "Latitude: {lat:.2f}, Longitude: {lng:.2f}.".format(lat=self.lat, lng=self.lng)


def sort_stops(your_lat, your_lng, route):
    day_week = date.today().strftime("%A")
    if (day_week == "Saturday" or day_week == "Sunday") and (route == "red" or route == "blue" or route == "green"):
        return "Sorry, this bus doesn't run on the weekend."
    try:
        coords = list(routes[route].values())
        coord_string = ""
        for i in range(len(coords)):
            if i != 0:
                coord_string += "|" + str(coords[i][0]) + ", " + str(coords[i][1])
            else:
                coord_string += str(coords[i][0]) + ", " + str(coords[i][1])
        stop_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={lat}, {lng}&destinations={dest}&mode={mode}&key={key}".format(
            lat=your_lat, lng=your_lng, dest=coord_string, mode='walking', key=GMaps_key)
        r = requests.get(stop_url)
        j = r.json()
        data = j["rows"][0]["elements"]
        distances = []
        travel_time = []

        for i in data:
            distances.append(i['distance']['value'])
            travel_time.append(i['duration']['value'])
        closest_stop_index = travel_time.index(min(travel_time))
        closest_stop_name = list(routes[route].keys())[closest_stop_index]
        closest_stop_coords = coords[closest_stop_index]

        ###
        bus_pos_r = requests.get("http://m.gatech.edu:80/api/buses/position")
        bus_pos_j = bus_pos_r.json()
        bus_coords = []
        for i in bus_pos_j:
            if i["route"] == route:
                bus_coords.append([i["lat"], i["lng"]])
        bus_coord_string = ""
        for i in range(len(bus_coords)):
            if i != 0:
                bus_coord_string += "|" + str(bus_coords[i][0]) + ", " + str(bus_coords[i][1])
            else:
                bus_coord_string += str(bus_coords[i][0]) + ", " + str(bus_coords[i][1])

        bus_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={lat}, {lng}&destinations={dest}&mode={mode}&key={key}".format(
            lat=closest_stop_coords[0], lng=closest_stop_coords[1], dest=bus_coord_string, mode='driving',
            key=GMaps_key)
        bus_r = requests.get(bus_url)
        bus_j = bus_r.json()
        bus_data = bus_j["rows"][0]["elements"]
        bus_distances = []
        bus_travel_time = []
        for i in bus_data:
            bus_distances.append(i['distance']['value'])
            bus_travel_time.append(1.05 * i['duration']['value'])

        minutes = int(min(bus_travel_time) / 60)
        seconds = int(min(bus_travel_time) % 60)
        ret = "A {r} bus will be arriving at {stop} in {m} minutes and {s} seconds.".format(r=route,
                                                                                            stop=closest_stop_name,
                                                                                            m=minutes,
                                                                                            s=seconds)
        ret = ret.replace("Dr.", "Drive")
        ret = ret.replace("Dr", "Drive")
        return ret
    except:
        return "Sorry, bus information could not be found at this time."

if __name__ == "__main__":
    u = User("112 Bobby Dodd Way NW, Atlanta, GA 30332")
    u_lat = u.lat
    u_lng = u.lng

    cs = sort_stops(u_lat, u_lng, "blue")
    print(cs)
