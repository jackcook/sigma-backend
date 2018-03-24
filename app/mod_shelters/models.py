class Shelter:

    def __init__(self, shelter_id, name, address, lat, lng, data):
        self.shelter_id = shelter_id
        self.name = name
        self.address = address
        self.lat = lat
        self.lng = lng
        self.data = data

    def serialize(self):
        return {
            "shelter_id": self.shelter_id,
            "name": self.name,
            "address": self.address,
            "lat": self.lat,
            "lng": self.lng,
            "data": self.data
        }
