# Setting Job parameters

This process specifies seer's running parameters.

## Request
```http
POST /api/job?admin_id=<ADMIN_ID>
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

## GET Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```

# Starting the job
Returns an error if the TYPE is empty. 
TYPE can be 'real' or 'simulation'.

## Request
```http
PUT /api/job?type=<TYPE>&admin_id=<ADMIN_ID>
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

## Request
```http
DEL /api/job?pause=<PAUSE>&admin_id=<ADMIN_ID>
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
