"""
Just prints out the GPS coordinates
"""
import time
from airsimgeo import AirSimGeoClient
SRID = 'EPSG:5555'
ORIGIN = (7.33577, 51.43672, 3.3)

def main():
    client = AirSimGeoClient(srid=SRID, origin=ORIGIN)
    client.confirmConnection()
    while True:
        pos = client.getGpsLocation()
        print("{:.4f},{:.4f},{:.4f}".format(pos[0], pos[1], pos[2]))
        time.sleep(2)   # delays for 5 seconds.

if __name__ == '__main__':
    main()