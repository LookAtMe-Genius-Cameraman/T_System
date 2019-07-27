# Creating new Scenario

Creates a new motion Scenario for T_System's arm to follow path during shoot with camera.

## Request
```http
POST /api/scenario?admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/json

{
    "name": "scenario_name",
    "positions": [
    {
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "position1_name",
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    },
    {
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "position2_name",
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    }],
}
```

## Response

### On Success
```json
{
  "status": "OK",
  "id": "b970138a-aecb-11e9-b130-cc2f714671ed"
}
```

### On failure
```json
{
    "status": "ERROR",
    "message": "Missing or incorrect parameters"
}
```

# Getting Devices
- If a specific parameter ID is given, its scenario are listed.

## Request
```http
GET /api/scenario?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
```json
{
    "status": "OK",
    "data":[
    {
    "id": "b97dr48a-aecb-11e9-b130-cc2f7156l1ed",
    "name": "scenario_name",
    "positions": [
    {
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "position1_name",
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    },
    {
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "position2_name",
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    }]
    }]
}
```
### On Failure
```json
{
    "status": "ERROR"
}
```

# Updating Scenario
Returns an error if the ID is empty.

## Request
```http
PUT /api/scenario?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/json

{
    "name": "scenario_name",
    "scenarios": [
    {
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "position1_name",
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    },
    {
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "position2_name",
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    }],
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

# Deleting scenario
Removes the scenario.

## Request
```http
DEL /api/scenario?id=<ID>&admin_id=<ADMIN_ID>
Content-Type: application/json
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
    "status": "ERROR",
    "message": "ID parameter is missing."
}
```
