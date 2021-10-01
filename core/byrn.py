# Byrn
# An extension of Solidpy for analyzing sounding rockets and solid rocket motors

from solidpy import *

class Motor:
    def __init__(self, source_filename, exhaust_area):
        self.model = Stl(source_filename)
        self.model.parse()
        self.exhaust_pressure = 0
        self.mass_flux = 0
        self.exhaust_velocity = 0
        self.exhaust_area = exhaust_area
        self.thrust = 0
        self.burn_area = self.model.compute_surface_area()
        self.volume = self.model.compute_volume()
        self.dt = 0.01
    def compute_mass_flux(self):
        pass # Units kg/s/m2
    def compute_exhaust_pressure(self):
        pass # Approximate steady state pressure
    def compute_exhaust_velocity(self):
        pass # Approximate steady state gas velocity
    def compute_thrust(self, backpressure):
        self.compute_mass_flux()
        self.compute_exhaust_pressure()
        self.compute_exhaust_velocity()
        self.thrust = self.mass_flux*self.exhaust_area*self.exhaust_velocity + (self.exhaust_pressure - backpressure)*self.exhaust_area
        return self.thrust
        
