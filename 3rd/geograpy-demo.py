#!/usr/bin/env python2
import geograpy
from geograpy import extraction
from geograpy import places

t = "Anhui bucuo, Hefei is good, Beijing is a good city, China is a good country, Asia is a good continent."

p = extraction.Extractor(text=t)

p.find_entities()

pp = places.PlaceContext(p.places)

pp.set_countries()
print pp.countries
pp.set_regions()
print pp.regions
try:
    pp.set_cities()
except Exception as e:
    pass
print pp.cities
