from schema import Schema, Use, Optional, And, Or


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

JOB_SCHEMA = Schema({
    'job_type': And(str, Use(str.lower), lambda s: s in ('track', 'learn', 'secure')),
    'scenario': Use(str),
    'predicted_mission': Use(bool),
    'recognized_persons': Or(None, Use(list)),
    'non_moving_target': Or(None, Use(bool)),
    'ai': Or(None, Use(str)),
})

FACE_ENCODING_SCHEMA = Schema({
    'face_name': Use(str),
    'photos': Use(list),
})

UPDATE_SCHEMA = Schema({
    'auto_update': Use(bool),
})

RECORD_SCHEMA = Schema({
    'name': Use(str),
})
