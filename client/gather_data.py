# This module gathers temperature and air pressure. 
# If bmp280 sensor not found, data will be downloaded from https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.9333&lon=10.7166
# Require data from bmp280 not tested yet!

import time, subprocess, json, platform, re
try:
    from bmp280 import BMP280
    from smbus import SMBus
except ModuleNotFoundError:
    print("BMP280 or smbus module not found!")

class Gather_data:
    def __init__(self, sensor=False):
        self.bus=None
        self.bmp280=None)
        if re.search("(?i)arm", platform.machine()):
            self.bus = SMBus(1)
            self.bmp280 = BMP280(i2c_dev=self.bus)
                
    def __gather_data_from_url(self):
        """
        gather latest temperature and pressure from Oslo. These are updated every 5 minutes

        :return: dict, air temperature in degree celsius, air pressure in hPa
        """
        output = subprocess.check_output(["curl -X GET --header \'Accept: application/json\' \'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.9333&lon=10.7166\'"], shell=True, stderr=subprocess.DEVNULL)

        data = json.loads(output)['properties']['timeseries'][0]['data']['instant']['details']
        return {'air_temperature': data['air_temperature'],
                'air_pressure': data['air_pressure_at_sea_level']}
    
    def gather(self):
        """
        Gathers time air temperature and air pressure either from sensor or from url

        :return: dict, current time in seconds since epoch, air temperature in degree celsius, air pressure in hPa
        """
        tm = {'time': time.time_ns()}
        if self.bmp280:
            tm.update({ 'air_temperature': self.bmp280.get_temperature(),
                        'air_pressure': self.bmp280.get_pressure()})
        else:
            tm.update(self.__gather_data_from_url())
        return tm
if __name__ == '__main__':
    g = Gather_data(sensor=True)
    data = g.gather()
    print(data)