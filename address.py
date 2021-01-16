import googlemaps

class Address:

    def __init__(self, name, soc, address, city, province, zip):
        self.name = name
        self.soc = soc
        self.address = address
        self.city = city
        self.province = province
        self.zip = zip


    def __get_geocode(self):
        KEY = 'AIzaSyABRC1BA_smOa1N8pBjP-Pvco4BNqb2l_s'

        gmaps = googlemaps.Client(key=KEY)
        
        gcode = gmaps.geocode(f"{self.address}, {self.city}, {self.province}")
        lat_long = gcode[0]["geometry"]["location"]

        return lat_long["lat"], lat_long["lng"]

    def __hash_zip_soc(self):
        return hash(self.zip), hash(self.soc)


    def return_val(self):
        lat, lng = self.__get_geocode()
        zip_hash, soc_hash = self.__hash_zip_soc()

        return (lat, lng, zip_hash, soc_hash)