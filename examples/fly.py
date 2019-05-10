"""
Flys to a georeferenced building in the Unreal Engine
"""
import time
from airsimgeo import AirSimGeoClient
SRID = 'EPSG:5555'
ORIGIN = (7.33577, 51.43672, 3.3)

def main():
    client = AirSimGeoClient(srid=SRID, origin=ORIGIN)
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    # Take off
    client.takeoffAsync(timeout_sec=5).join()
    gps = client.getGpsLocation()
    # Go up by 15 meters
    gps_new = (gps[0], gps[1], gps[2] + 15.0)
    print("Going Higher")
    client.moveToPositionAsyncGeo(gps=gps_new, velocity=5).join()
    # Move to new position
    gps_new = (7.33709, 51.43735, 22.0)
    print("Moving")
    client.moveToPositionAsyncGeo(gps=gps_new, velocity=10,).join()
    # Land, doesn't seem to work....
    time.sleep(5)
    print("Landing")
    client.landAsync().join()


if __name__ == '__main__':
    main()