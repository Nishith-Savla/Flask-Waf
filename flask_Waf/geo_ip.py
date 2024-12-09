import geoip2.database

class GeoIPDatabase:
    def __init__(self, database_path):
        self.reader = geoip2.database.Reader(database_path)

    def lookup(self, ip_address):
        try:
            response = self.reader.country(ip_address)
            return response.country.iso_code
        except geoip2.errors.AddressNotFoundError:
            return None

    def __del__(self):
        self.reader.close()

