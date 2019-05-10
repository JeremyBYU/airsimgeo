

from airsim import Vector3r, MultirotorClient
from pyproj import Proj

class AirSimGeoClient(MultirotorClient):
    def __init__(self, srid, origin, **kwargs):
        """AirSim client that understands arbitrary projection systems
        Assumes that the simulation environment (unreal) is in the coordinate system specified
        by the srid but offset by the origin specified.
        Arguments:
            srid {str} -- EPSG SRID string. Example "EPSG:3857"
            origin {list} -- [Longitude, Latitude, Height]
            kwargs -- Any keyword arguments forwared to AirSim
        """

        self.srid = srid
        self.origin = origin

        self.proj = Proj(init=srid)
        self.origin_proj = self.proj(*self.origin[0:2]) + (self.origin[2],)

        super(AirSimGeoClient, self).__init__(**kwargs)

    def lonlatToProj(self, lon, lat, z, inverse=False):
        proj_coords = self.proj(lon, lat, inverse=inverse)
        return proj_coords + (z,)

    def projToAirSim(self, x, y, z):
        x_airsim = x - self.origin_proj[0]
        y_airsim = y - self.origin_proj[1]
        z_airsim = -z + self.origin_proj[2]
        return (x_airsim, -y_airsim, z_airsim)

    def lonlatToAirSim(self, lon, lat, z):
        return self.projToAirSim(*self.lonlatToProj(lon, lat, z))

    def nedToProj(self, x, y, z):
        """
        Converts NED coordinates to the projected map coordinates
        Takes care of offset origin, inverted z, as well as inverted y axis
        """
        x_proj = x + self.origin_proj[0]
        y_proj = -y + self.origin_proj[1]
        z_proj = -z + self.origin_proj[2]
        return (x_proj, y_proj, z_proj)

    def nedToGps(self, x, y, z):
        return self.lonlatToProj(*self.nedToProj(x, y, z), inverse=True)

    def getGpsLocation(self):
        """
        Gets GPS coordinates of the vehicle.
        """
        pos = self.simGetGroundTruthKinematics().position
        gps = self.nedToGps(pos.x_val, pos.y_val, pos.z_val)
        return gps

    def moveToPositionAsyncGeo(self, gps=None, proj=None, **kwargs):
        """
        Moves to the a position that is specified by gps (lon, lat, +z) or by the projected map 
        coordinates (x, y, +z).  +z represent height up.
        """
        coords = None
        if gps is not None:
            coords = self.lonlatToAirSim(*gps)
        elif proj is not None:
            coords = self.projToAirSim(*proj)
        if coords:
            return self.moveToPositionAsync(coords[0], coords[1], coords[2], **kwargs)
        else:
            print('Please pass in GPS (lon,lat,z), or projected coordinates (x,y,z)!')

    def moveOnPathAsyncGeo(self, gps=None, proj=None, velocity=10, **kwargs):
        """
        Moves to the a path that is a list of points. The path points are either gps (lon, lat, +z) or by the projected map 
        coordinates (x, y, +z).  +z represent height is up.
        """
        path = None
        if gps is not None:
            path = [Vector3r(*self.lonlatToAirSim(*cds)) for cds in gps]
        elif proj is not None:
            path = [Vector3r(*self.projToAirSim(*cds)) for cds in proj]
        if path:
            # print(gps, path)
            return self.moveOnPathAsync(path, velocity=velocity, **kwargs)
        else:
            print(
                'Please pass in GPS [(lon,lat,z)], or projected coordinates [(x,y,z)]!')