from schema import Schema, Use, Optional


POSITION_SCHEMA = Schema({
    'name': Use(str),
    'cartesian_coords': Use(list),
    'polar_coords': Use(list),
})

SCENARIO_SCHEMA = Schema({
    'name': Use(str),
    'positions': Use(list),
})

MOVE_SCHEMA = Schema({
    'type': Use(str),
    'id': Use(str),
    'quantity': Use(int),
})

NETWORK_SCHEMA = Schema({
    'ssid': Use(str),
    'password': Use(str),
})

# LOCATION_SCHEMA = Schema({
#     'name': Use(str),
#     'ip': Use(str),
#     Optional('description'): Use(str),
# })
