# Setting Job parameters

This process specifies seer's running parameters.
If the MARK parameter is full, it changes the mark type of the place that is around of the found object on screen.

## Request
```http
POST /api/job?mark=<MARK>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/json; charset=UTF-8

{
    "job_type": "track" / "learn" / "secure",
    "scenario": "scenario_1",
    "predicted_mission": False,
    "recognized_persons": None / ["all"] / [o953417h-aegb-21e6-b537-ct2g614671ed", "b970538v-aecb-11r6-b130-fc2f713571ed"],
    "non_moving_target": None / False,
    "ai": None / "official_ai"
}
```
## Response

### On Success
```json
{
  "status": "OK"
}
```

### On failure
```json
{
    "status": "ERROR"
}
```

## Getting Target Marks 
```http
GET /api/job?cause=<CAUSE>&admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
- If CAUSE is 'mark'
```json
{
    "status": "OK",
    "data": [
    "single_rect",
    "partial_rect",
    "rotating_arcs",
    {
      "animations": [
        "animation_1"
      ]
    }
  ]
}
```

# Starting the job
Returns an error if the CAUSE is empty. 
CAUSE can be 'take_shots', 'track', 'record' or 'mission'.

If CAUSE is;
'take_shots' : Takes single photo.
'track': Starts searching and tracking object works.
'record': Starts video recording works.
'mission': Starts T_System's Arm mission.
'live_stream': Starts T_System's Live Streaming.

## Request
```http
PUT /api/job?cause=<CAUSE>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

{
}
```

## Response
### On Success
```json
{
    "status": "OK"
}
```

### On Failure
```json
{
    "status": "ERROR"
}
```

# Resuming the paused job

## Request
```http
PATCH /api/job?admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

{
}
```

## Response
### On Success
```json
{
    "status": "OK"
}
```

### On Failure
```json
{
    "status": "ERROR"
}
```

# Stopping/Pausing the job
If the PAUSE parameter is not None, job will pause.
CAUSE can be, 'track', 'record' or 'mission'.

If CAUSE is;
'track': Stops searching and tracking object works.
'record': stops video recording works.
'mission': Stops T_System's Arm mission.
'live_stream': Stops T_System's Live Streaming.

## Request
```http
DEL /api/job?pause=<PAUSE>&cause=<CAUSE>&admin_id=<ADMIN_ID>
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
```

## Response
### On Success
```json
{
    "status": "OK"
}
```
### On Failure
```json
{
    "status": "ERROR"
}
```
