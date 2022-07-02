# This module gathers temperature and air pressure. 
# If bmp280 sensor not found, data will be downloaded from https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.9333&lon=10.7166
# Require data from bmp280 not tested yet!

import time, subprocess, json

class Gather_data:
    def __init__(self):
        self.sensor=True
        self.bus=None
        self.bmp280=None

        try:
            from bmp280 import BMP280
        except ModuleNotFoundError:
            print("BMP280 module not found!")
            self.sensor=False

        if self.sensor:
            try:
                from smbus2 import SMBus
            except ImportError:
                from smbus import SMBus
            self.bus = SMBus(1)
            self.bmp280 = BMP280(i2c_dev=bus)
                
    # gather latest temperature and pressure from Oslo. These are updated every 5 minutes
    def __gather_data_from_url(self):
        output = subprocess.check_output(["curl -X GET --header \'Accept: application/json\' \'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.9333&lon=10.7166\'"], shell=True, stderr=subprocess.DEVNULL)

        data = json.loads(output)['properties']['timeseries'][0]['data']['instant']['details']
        return (data['air_temperature'], data['air_pressure_at_sea_level'])
    
    def gather(self):
        tm = time.time()
        if self.sensor:
            return (tm, self.bmp280.get_temperature(), self.bmp280.get_pressure())
        
        return (tm,) + self.__gather_data_from_url()

if __name__ == '__main__':
    g = Gather_data()
    data = g.gather()
    print(data)