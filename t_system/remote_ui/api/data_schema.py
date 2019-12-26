from schema import Schema, Use, Optional, And, Or


POSITION_SCHEMA = Schema({
    'name': Use(str),
    'cartesian_coords': Use(list),
    'polar_params': Use(dict),
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
    'scenario': Or(None, Use(str)),
    'predicted_mission': Use(bool),
    'recognized_persons': Or(None, Use(list)),
    'non_moving_target': Or(None, Use(bool)),
    Optional('arm_expansion'): Or(None, Use(bool)),
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

ACCESS_SCHEMA = Schema({
    'id': Use(str)
})

IDENTITY_SCHEMA = Schema({
    'public_id': Or(None, Use(str)),
    'private_id': Or(None, Use(str)),
    'name': Or(None, Use(str))
})

L_STREAM_SCHEMA = Schema({
    'account_name': Use(str),
    'key': Use(str)
})

L_S_WEBSITE_SCHEMA = Schema({
    'name': Use(str),
    'url': Use(str),
    'server': Use(str)
})

SYNC_ACCOUNT_SCHEMA = Schema({
    'name': Use(str),
    'key': Use(str)
})
